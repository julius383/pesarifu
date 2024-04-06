import datetime
import functools
import json
import logging.config
import os
import re
import time
from contextlib import contextmanager
from itertools import takewhile
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional
from uuid import uuid4

import pandas as pd
import structlog
import tabula
from pypdf import PdfReader, PdfWriter

# from icecream import ic
from thefuzz import fuzz
from toolz import keyfilter, pipe

from pesarifu.config.config import settings


def configure_logger():
    if (level := settings.get("LOG_LEVEL", None)) is None:
        level = "INFO"
    else:
        level = level.upper()
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "plain": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(colors=False),
                    ],
                },
                "json_formatter": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processor": structlog.processors.JSONRenderer(),
                },
                "colored": {
                    "()": structlog.stdlib.ProcessorFormatter,
                    "processors": [
                        structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                        structlog.dev.ConsoleRenderer(colors=True),
                    ],
                },
            },
            "handlers": {
                "default": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "colored",
                },
                "file": {
                    "level": "DEBUG",
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": "logs/pesarifu-text.log",
                    "formatter": "plain",
                },
                "json_file": {
                    "level": "DEBUG",
                    "class": "logging.handlers.WatchedFileHandler",
                    "filename": "logs/pesarifu-json.log",
                    "formatter": "json_formatter",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["default", "file", "json_file"],
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        }
    )

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                ]
            ),
            structlog.processors.dict_tracebacks,
            structlog.processors.format_exc_info,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.UnicodeDecoder(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        cache_logger_on_first_use=True,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )
    os.makedirs(os.path.join(settings.APP_ROOT, "logs"), exist_ok=True)
    return structlog.get_logger()


logger = configure_logger()


class ParseError(Exception):
    """Error raised when some input can't be parsed into the expected object"""


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


def omit(blacklist, d):
    return keyfilter(lambda k: k not in blacklist, d)


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.timestamp()
    raise TypeError(repr(obj) + " is not JSON serializable")


def normalize_key(key: Any) -> str:
    return re.sub(
        r"[:]",
        "",
        re.sub(r"\s", "_", re.sub(r"\s{2,}", " ", str(key).lower().strip())),
    )


def normalize_name(name: str) -> str:
    return pipe(
        name, lambda x: re.sub(r"lull", "", x, re.IGNORECASE), str.title
    )


def convert_to_cash(v: str | float) -> Optional[float]:
    try:
        result = None
        if isinstance(v, float):
            result = v
        elif isinstance(v, int):
            result = float(v)
        elif isinstance(v, str):
            cleaned = re.sub(r"\s|[^0-9.-]", "", v)
            result = float(cleaned)
        else:
            raise ValueError
        return result
    except ValueError:
        logger.exception(f"Unable to convert {v} of type {type(v)} to float")


def is_header(header1: str, header2: str) -> bool:
    """Returns True if header1 and header2 are similar."""
    return any(
        fuzz.ratio(x, y) >= 60 and abs(len(x) - len(y)) <= 3
        for (x, y) in zip(
            map(normalize_key, header1), map(normalize_key, header2)
        )
    )


# https://realpython.com/primer-on-python-decorators/#decorators-with-arguments
def save_results(path: str):
    """Decorator that saves output of function to `path` as json"""

    def decorator_save_output(func):
        @functools.wraps(func)
        def wrapper_save_output(*args, **kwargs):
            res = func(*args, **kwargs)
            to = Path(path).expanduser()
            try:
                if to.exists():
                    new_path = to.with_stem(
                        f"{to.stem}-{int(time.monotonic())}"
                    )
                    logger.info(
                        f"{path} already exists writing to {new_path}",
                        func_name=func.__name__,
                    )
                    to = new_path
                with open(
                    to.with_suffix(".json"), "w", encoding="utf-8"
                ) as fp:
                    json.dump(res, fp)
                    logger.info(
                        f"Results written to {to}", func_name=func.__name__
                    )
            except TypeError:
                logger.exception("Could not encode json")
            return res

        return wrapper_save_output

    return decorator_save_output


def count_empty(d: dict) -> int:
    count = 0
    for i in d.values():
        if not bool(i) or (isinstance(i, float) and math.isnan(i)):
            count += 1
    return count


def read_pdf(
    file: Path,
    columns_xcoords: List[int],
    column_names: List[str],
    pages="all",
    join_consecutive_on: Optional[str] = None,
) -> List[Dict[str, str | int | float]]:
    """Reads transactions from a PDF file.

    Uses tabula to read tables from a PDF file and process them into the a list of
    dictionaries.

    Args:
        file: A Path to the PDF file that will be opened for reading
        columns_xcoords: A list of x-coordinates for the columns in the PDF tables.
          Passed to tabula.read_pdf
        pages: A string defining which pages to process see `tabula.read_pdf` for
          options. Passed to tabula.read_pdf
        column_names: A list of the column names in the PDF table.
        join_consecutive_on: The column that will be combined with the previous row.

    Returns:
        A list of dicts with each item corresponding to a rows in the tables.
    """
    tables: list[pd.DataFrame] = tabula.read_pdf(  # noqa
        file, pages=pages, columns=columns_xcoords
    )
    column_names = [normalize_key(i) for i in column_names]
    results = []
    # TODO: try and simplfy the code below
    for table in tables:
        for col in table.columns:
            if pd.isna(table[col]).all():
                del table[col]
        if len(table.columns) != len(columns_xcoords):
            continue
        table.columns = column_names
        if join_consecutive_on:
            table.dropna(subset=[join_consecutive_on], inplace=True)
        records = table.to_dict("records")
        rec_width = len(columns_xcoords)
        index = 0
        while index < len(records):
            record = records[index]
            empty = count_empty(record)
            if empty >= rec_width // 2 or is_header(
                record.values(), column_names
            ):
                index += 1
                continue
            if join_consecutive_on:
                try:
                    to_join = map(
                        lambda x: x.get(join_consecutive_on),
                        takewhile(
                            lambda x: count_empty(x) > rec_width // 2,
                            records[index + 1 :],
                        ),
                    )
                    record[join_consecutive_on] += " " + " ".join(to_join)
                except IndexError:
                    pass
            results.append(record)
            index += 1
    return results


def decrypt_pdf(data: BinaryIO, password: str | None) -> Path:
    """Decrypt PDF and copy it to statements directory."""
    reader = PdfReader(data)
    writer = PdfWriter()
    uuid = uuid4()
    if reader.is_encrypted:
        if password is None:
            raise KeyError("Password not provided for encrypted pdf")
        reader.decrypt(password)
    for page in reader.pages:
        writer.add_page(page)
    ofile = settings.STATEMENTS_BASE_DIR / Path(uuid.hex).with_suffix(".pdf")
    with open(ofile, "wb") as fp:
        writer.write(fp)
    return ofile


def nothing(**kwargs):
    for k, v in kwargs.items():
        logger.info(f"doing nothing on %s=%s", k, v)
    return


def format_timestamp(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    # https://stackoverflow.com/a/739266
    if 4 <= dt.day <= 20 or 24 <= dt.day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][dt.day % 10 - 1]
    return dt.strftime(f"%B %-d{suffix}, %Y")


# https://stackoverflow.com/a/24176022
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)
