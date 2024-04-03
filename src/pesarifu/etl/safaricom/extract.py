from pathlib import Path
from typing import Any, Dict

# from icecream import ic
from sh import ErrorReturnCode, pdftotext, sed

from pesarifu.etl.safaricom.transform import parse_date, parse_phone
from pesarifu.util.helpers import normalize_key, normalize_name, read_pdf, save_results


# @save_results("~/code/Python/pesarifu-dev/pesarifu/transactions")
def get_transactions_from_pdf(path: Path) -> list[Dict[str, Any]]:
    columns = [
        36,
        117,
        197,
        358,
        440,
        480,
        519,
    ]
    records: list[Dict[str, Any]] = read_pdf(
        path,
        columns_xcoords=columns,
        column_names=[
            "Receipt No",
            "Completion Time",
            "Details",
            "Transaction Status",
            "Paid In",
            "Withdrawn",
            "Balance",
        ],
        join_consecutive_on="details",
        # pages="1-3",
    )
    return records


# @save_results("~/code/Python/pesarifu-dev/pesarifu/metadata")
# TODO: cache results of this function
def get_metadata_from_pdf(path: Path) -> dict[str, Any]:
    "Extract user information from header in Mpesa statement"
    try:
        output = sed(
            "-E",
            "-n",
            "-e",
            "/.*PESA.*STATEMENT/,/^SUMMARY/p",
            _in=pdftotext("-f", 1, "-l", 1, path, "-"),
        )
    except ErrorReturnCode as e:
        raise ValueError from e
    if not output:
        raise ValueError
    lines: list[str] = output.strip().split("\n")
    cleaned_lines = list(filter(bool, lines[1:-2]))
    keys = list(filter(lambda x: x.endswith(":"), cleaned_lines))
    values = list(filter(lambda x: not x in keys, cleaned_lines))
    metadata: dict[str, Any] = dict(zip(map(normalize_key, keys), values))
    metadata["customer_name"] = normalize_name(metadata["customer_name"])
    metadata["mobile_number"] = parse_phone(metadata["mobile_number"])
    metadata["date_of_statement"] = (
        parse_date(metadata["date_of_statement"])
        if "date_of_statement" in metadata.keys()
        else parse_date(metadata["request_date"])
    )
    start, end = metadata["statement_period"].split(" - ")
    metadata["statement_period"] = {
        "start_ts": parse_date(start),
        "end_ts": parse_date(end),
    }
    return metadata
