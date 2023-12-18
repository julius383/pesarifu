from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional
import re

from dateutil.parser import isoparse
from icecream import ic
from sh import pdftotext, sed
from toolz import update_in

from pesarifu.util.helpers import (
    convert_to_cash,
    normalize_key,
    read_pdf,
    save_results,
    ParseError,
)


@save_results("~/code/Python/pesarifu-dev/pesarifu/transactions")
def get_transactions_from_pdf(path: Path) -> List[Dict[str, Any]]:
    columns = [
        36,
        117,
        197,
        358,
        440,
        480,
        519,
    ]
    records: List[Dict[str, Any]] = read_pdf(
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
    )
    transactions = []
    for record in records:
        ic(record)
        transaction = {
            "transaction_id": record["receipt_no"],
            "amount": convert_to_cash(record["paid_in"])
            - convert_to_cash(record["withdrawn"]),
            "initiated_at": isoparse(record["completion_time"] + "Z"),
            "details": record["details"],
            "metadata": {
                "balance_at": convert_to_cash(record["balance"]),
            },
        }
        transactions.append(transaction)
    return transactions


def parse_date(date: str) -> datetime:
    "Parse date format found in Mpesa statement"
    p = re.compile(r"(?P<day>\d{2})[a-z]{2}\s+(?P<month>\d)\s+(?P<year>\d{4})")
    match = re.match(p, date)
    if match:
        return datetime(
            *map(
                int,
                [
                    match.group("year"),
                    match.group("month"),
                    match.group("day"),
                ],
            )
        )
    raise ParseError(f"{date} does not match expected pattern {p}")


def parse_phone(number: str) -> str:
    "Parse mobile number found in Mpesa statement"
    p = re.compile(r"(?P<code>\d{3})(?P<number>\d{9})")
    match = re.match(p, number)
    if match:
        return f"+{match.group('code')} {match.group('number')}"
    raise ParseError(f"{number} does not match expected pattern {p}")


def get_metadata_from_pdf(path: Path) -> dict[str, Any] | None:
    "Extract user information from header in Mpesa statement"
    output = sed(
        "-E",
        "-n",
        "-e",
        "/^MPESA FULL STATEMENT/,/^SUMMARY/p",
        _in=pdftotext("-f", 1, "-l", 1, path, "-"),
    )
    lines: list[str] = output.strip().split("\n")
    cleaned_lines = list(filter(bool, lines[1:-2]))
    if len(cleaned_lines) % 2 != 0:
        raise ValueError
    mid = len(cleaned_lines) // 2
    metadata: dict[str, Any] = dict(
        zip(map(normalize_key, cleaned_lines[:mid]), cleaned_lines[mid:])
    )
    metadata["customer_name"] = str.title(metadata["customer_name"])
    metadata["mobile_number"] = parse_phone(metadata["mobile_number"])
    metadata["date_of_statement"] = parse_date(metadata["date_of_statement"])
    start, end = metadata["statement_period"].split(" - ")
    metadata["statement_period"] = {
        "start": parse_date(start),
        "end": parse_date(end),
    }
    return metadata


# TODO: move to transform.py?
def get_transaction_from_api(
    json_obj: Dict[str, str]
) -> Optional[Dict[str, Decimal | str]]:
    if not set(
        [
            "TransactionType",
            "TransID",
            "TransTime",
            "TransAmount",
            "BusinessShortCode",
            "BillRefNumber",
            "MSISDN",
            "FirstName",
            "MiddleName",
            "LastName",
        ]
    ) <= set(json_obj.keys()):
        return
    transaction = {}
    dt = json_obj["TransTime"]
    if json_obj["BillRefNumber"]:
        transaction["account"] = {
            "paybill_number": json_obj["BusinessShortCode"],
            "account_number": json_obj["BillRefNumber"],
        }
    else:
        transaction["account"] = {
            "till_number": json_obj["BusinessShortCode"],
        }
    transaction |= {
        "transaction_id": json_obj["TransID"],
        "amount": convert_to_cash(json_obj["TransAmount"]),
        "initiated_at": isoparse(dt[:8] + "T" + dt[8:]),
        "initiator": {
            "mobile_user": {
                "name": " ".join(
                    [
                        json_obj["FirstName"],
                        json_obj["MiddleName"],
                        json_obj["LastName"],
                    ]
                ),
                "number": json_obj["MSISDN"],
            }
        },
    }
    return transaction
