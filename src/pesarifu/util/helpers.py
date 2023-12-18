import datetime
import functools
import math
import re
import time
from decimal import Decimal
from itertools import takewhile
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd
import simplejson as json
import tabula

# from icecream import ic
from thefuzz import fuzz


class ParseError(Exception):
    """Error raised when some input can't be parsed into the expected object"""
    pass


def encode_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.timestamp()
    raise TypeError(repr(obj) + " is not JSON serializable")


def normalize_key(key: Any) -> str:
    return re.sub(
        r"[:]",
        "",
        re.sub(
            r"\s",
            "_",
            re.sub(
                r"\s{2,}",
                " ",
                str(key).lower().strip()
            )
        )
    )


def convert_to_cash(v: str | float | Decimal) -> Decimal:
    if isinstance(v, Decimal):
        return v
    elif isinstance(v, float) or isinstance(v, int):
        return Decimal(v)
    elif isinstance(v, str):
        cleaned = re.sub(r"\s|[^0-9.-]", "", v)
        return Decimal(cleaned)
    else:
        raise ValueError(f"Can't convert {v} of type {type(v)} to Decimal")


def is_header(header1: str, header2: str) -> bool:
    """Returns True if header1 and header2 are similar."""
    return any(
        [
            fuzz.ratio(x, y) >= 60 and abs(len(x) - len(y)) <= 3
            for (x, y) in zip(
                map(normalize_key, header1), map(normalize_key, header2)
            )
        ]
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
                        f"{to.stem}-{int(time.monotonic())}")
                    print(f"{path} already exists writing to {new_path}")
                    to = new_path
                with open(to.with_suffix('.json'), 'w', encoding='utf-8') as fp:
                    json.dump(res, fp, default=encode_datetime)
                    print(f"Results written to {to}")
            except TypeError:
                print("Could not encode json")
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
    # TODO: handle table with info related to owner of PDF
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
                            records[index + 1:],
                        ),
                    )
                    record[join_consecutive_on] += " " + " ".join(to_join)
                except IndexError:
                    pass
            results.append(record)
            index += 1
    return results
