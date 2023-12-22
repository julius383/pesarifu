import re
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from dateutil.parser import isoparse

from pesarifu.util.helpers import (
    ParseError,
    convert_to_cash,
    normalize_key,
    save_results,
)

# TODO: write export for excel, csv and jsonl
# TODO: align fields in JSON and PDF extract
# TODO: use models from models.py


def parse_details(details: str):
    details = details.strip()
    details = re.sub(r"\s+|\\", " ", details)
    re_flags = re.IGNORECASE
    patterns = {
        # TODO: convert capture groups to named ones and build object
        "customer-transfer": re.compile(
            r"Customer Transfer to ([*0-9]{12}) - (.*)$", re_flags
        ),
        "funds-received": re.compile(
            r"Funds received from ([*0-9]{12}) - (.*)$", re_flags
        ),
        "merchant-payment": re.compile(
            r"Merchant Payment Online to ([0-9]{6,8}) - (.*)$", re_flags
        ),
        "customer-payment": re.compile(
            r"Customer Payment to Small Business to ([*0-9]{10}) - (.*)$",
            re_flags,
        ),
        "paybill-online": re.compile(
            r"Pay Bill Online to ([0-9]{6,8}) - ((?:\w+\s+)+)Acc\.\s+(\w+)$",
            re_flags,
        ),
        "business-payment": re.compile(
            r"(?:Business|Salary) Payment from ([0-9]{6,8}) - ((?:\w+\s+)+)via (.*).$",
            re_flags,
        ),
    }

    for k, v in patterns.items():
        match = re.match(v, details)
        if match:
            groups = match.groups()
            return k, groups
        elif not re.search(r"[0-9]+", details):
            return ("misc-item", details)
    return ("parse-failure", details)


def parse_date(date: str) -> float:
    "Parse date format found in Mpesa statement"
    p = re.compile(r"(?P<day>\d{2})[a-z]{2}\s+(?P<month>\d)\s+(?P<year>\d{4})")
    match = re.match(p, date)
    if match:
        return datetime(
            year=int(match.group("year")),
            month=int(match.group("month")),
            day=int(match.group("day")),
        ).timestamp()
    raise ParseError(f"{date} does not match expected pattern {p}")


def parse_phone(number: str) -> str:
    "Parse mobile number found in Mpesa statement"
    p = re.compile(r"(?P<code>\d{3})(?P<number>\d{9})")
    match = re.match(p, number)
    if match:
        return f"+{match.group('code')} {match.group('number')}"
    raise ParseError(f"{number} does not match expected pattern {p}")


def transform_pdf_record(record):
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
    return transaction


def transform_api_record(
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
