import datetime
import functools
import json
import logging
import math
import re
import time
from datetime import timezone
from itertools import takewhile
from pathlib import Path
from typing import Any, BinaryIO, Dict, List, Optional
from uuid import uuid4

import pandas as pd
import structlog
import tabula
from dotenv import dotenv_values, find_dotenv
from pypdf import PdfReader, PdfWriter

# from icecream import ic
from thefuzz import fuzz
from toolz import keyfilter

ROOT_DIR: Path = Path(find_dotenv(".env")).absolute().parent
STATEMENTS_BASE_DIR = ROOT_DIR / "statements"
CONFIG: dict[str, str | None] = dotenv_values(".env")


def configure_logger():
    if (level := CONFIG.get("LOG_LEVEL", None)) is None:
        level = "INFO"
    else:
        level = level.upper()
    log_level = getattr(logging, level)
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            structlog.processors.TimeStamper(
                fmt="%Y-%m-%d %H:%M:%S", utc=False
            ),
            structlog.dev.ConsoleRenderer(),
        ],
    )
    return structlog.get_logger()


logger = configure_logger()


class CustEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.replace(tzinfo=timezone.utc).timestamp()
        return json.JSONEncoder.default(self, o)


class ParseError(Exception):
    """Error raised when some input can't be parsed into the expected object"""


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


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


def convert_to_cash(v: str | float) -> float:
    if isinstance(v, float):
        return v
    if isinstance(v, int):
        return float(v)
    if isinstance(v, str):
        cleaned = re.sub(r"\s|[^0-9.-]", "", v)
        return float(cleaned)
    msg = f"Unable to convert {v} of type {type(v)} to float"
    logger.error(msg)
    raise ValueError(msg)


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
                    logger.info(f"{path} already exists writing to {new_path}")
                    to = new_path
                with open(
                    to.with_suffix(".json"), "w", encoding="utf-8"
                ) as fp:
                    json.dump(res, fp)
                    logger.info(f"Results written to {to}")
            except TypeError as e:
                logger.error("Could not encode json", e)
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
        if len(table.columns) != len(columns_xcoords):
            continue
        table.columns = column_names
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
    ofile = STATEMENTS_BASE_DIR / Path(uuid.hex).with_suffix(".pdf")
    with open(ofile, "wb") as fp:
        writer.write(fp)
    return ofile
