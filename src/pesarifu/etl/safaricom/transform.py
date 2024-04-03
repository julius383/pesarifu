import re
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Dict, Optional

from dateutil.parser import isoparse

# from icecream import ic
from toolz import pipe

from pesarifu.util.helpers import ParseError, convert_to_cash, logger

# TODO: align fields in JSON and PDF extract


class TransactionTypes(Enum):
    MOBILE_TRANSFER = auto()
    BUYGOODS_TRANSFER = auto()
    PAYBILL_TRANSFER = auto()
    SAFARICOM_TRANSFER = auto()


# @save_results("~/code/Python/pesarifu-dev/pesarifu/details-parse")
def parse_details(details: str) -> tuple[TransactionTypes, dict[str, str]]:
    details = details.strip()
    details = re.sub(r"\s+|\\", " ", details)
    re_flags = re.IGNORECASE
    patterns = [
        (
            TransactionTypes.MOBILE_TRANSFER,
            re.compile(
                r"Customer Transfer to (?P<maybe_number>[*0-9]{10,12}) - (?P<account_name>.*)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.MOBILE_TRANSFER,
            re.compile(
                r"Funds received from (?P<maybe_number>[*0-9]{10,12}) - (?P<account_name>.*)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.MOBILE_TRANSFER,
            re.compile(
                r"Send Money Reversal via API to (?P<maybe_number>[*0-9]{10,12}) - (?P<account_name>.*)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.BUYGOODS_TRANSFER,
            re.compile(
                r"Merchant Payment (?:Online )?to (?P<buygoods_number>[0-9]{6,8}) - (?P<account_name>.*)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.MOBILE_TRANSFER,
            re.compile(
                r"Customer Payment to Small Business to (?P<maybe_number>[*0-9]{10,12}) - (?P<account_name>.*)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.PAYBILL_TRANSFER,
            re.compile(
                r"Pay Bill (?:Online )?to (?P<paybill_number>[0-9]{6,8}) - (?P<account_name>(?:.+\s+)+)Acc\.\s+(?P<account_number>.+)$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.BUYGOODS_TRANSFER,
            re.compile(
                r"(?:Business|Salary|Promotion) Payment from (?P<buygoods_number>[0-9]{6,8}) - (?P<account_name>(?:.+\s+)+)via (?P<detail>.*).$",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Pay Utility Reversal.*)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Customer Transfer of Funds Charge)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Airtime Purchase)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Pay Bill Charge)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Withdrawal Charge)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>Buy Bundles Online)",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"(?P<purpose>M-Shwari (?:Withdraw|Deposit))",
                re_flags,
            ),
        ),
        (
            TransactionTypes.SAFARICOM_TRANSFER,
            re.compile(
                r"^(?P<purpose>Customer Withdrawal .*)",
                re_flags,
            ),
        ),
    ]

    for k, v in patterns:
        match = re.match(v, details)
        if match:
            return k, match.groupdict()
    raise ParseError(details)


def parse_date(date: str) -> float:
    months = {
        "Jan": 1,
        "Feb": 2,
        "Mar": 3,
        "Apr": 4,
        "May": 5,
        "Jun": 6,
        "Jul": 7,
        "Aug": 8,
        "Sep": 9,
        "Oct": 10,
        "Nov": 11,
        "Dec": 12,
    }
    "Parse date format found in Mpesa statement header"
    p = re.compile(
        r"(?P<day>\d{2})(?:[a-z]{2})?\s+(?P<month>\d+|\w{3})\s+(?P<year>\d{4})"
    )
    match = re.match(p, date)
    if match:
        year = int(match.group("year"))
        try:
            month = int(match.group("month"))
        except ValueError:
            month = int(months[match.group("month")])
        day = int(match.group("day"))
        return datetime(
            year=year,
            month=month,
            day=day,
        ).timestamp()
    raise ParseError(f"{date} does not match expected pattern {p}")


def parse_phone(number: str) -> str:
    "Parse mobile number found in Mpesa statement"
    p1 = re.compile(r"(?P<code>\d{3})(?P<number>\d{9})")
    p2 = re.compile(r"(?P<code>0)(?P<number>\d{9})")
    for p in [p1, p2]:
        match = re.match(p, number)
        if match:
            code = match.group("code") if match.group("code") != "0" else "254"
            phone = match.group("number")
            return f"+{code} {phone}"
    raise ParseError(f"{number} does not match expected pattern")


def transform_pdf_record(record):
    transaction = {
        "transaction_reference": record["receipt_no"],
        "amount": convert_to_cash(record["paid_in"])
        - convert_to_cash(record["withdrawn"]),
        "initiated_at": isoparse(record["completion_time"] + "+03:00"),
        "original_detail": record["details"],
        "extra": {
            "balance_at": convert_to_cash(record["balance"]),
        },
    }
    try:
        ttype, info = parse_details(record["details"])
        transaction["initiated_at"] = (
            transaction["initiated_at"]
            .replace(tzinfo=timezone.utc)
            .timestamp()
        )
        match ttype:
            case TransactionTypes.MOBILE_TRANSFER:
                info["maybe_number"] = pipe(
                    info["maybe_number"],
                    str.lower,
                    lambda x: re.sub(
                        r"(?:^|\s)([a-zA-Z])",
                        lambda x: str.upper(x.group(0)),
                        x,
                    ),  # Better Title Case than str.title
                    lambda x: re.sub(r"^0", "254", x),
                    lambda x: re.sub(r"^7", "2547", x),
                )
                if not re.search(r"\*\*\*", info["maybe_number"]):
                    info["phone_number"] = info["maybe_number"]
                if re.search(
                    r"small business",
                    transaction["original_detail"],
                    flags=re.IGNORECASE,
                ):
                    transaction["extra"]["pochi_la_biashara"] = True
                info["account_name"] = pipe(
                    info["account_name"], str.strip, str.title
                )
            case (
                TransactionTypes.BUYGOODS_TRANSFER
                | TransactionTypes.PAYBILL_TRANSFER
            ):
                info["account_name"] = pipe(info["account_name"], str.strip)
            case TransactionTypes.SAFARICOM_TRANSFER:
                transaction["purpose"] = info["purpose"]
    except ParseError as e:
        logger.warning("Unable to parse record %s", record)
        return
    transaction["other_account"] = info
    return transaction


def transform_api_record(
    json_obj: Dict[str, str]
) -> Optional[Dict[str, float | str]]:
    # if not set(
    #     [
    #         "TransactionType",
    #         "TransID",
    #         "TransTime",
    #         "TransAmount",
    #         "BusinessShortCode",
    #         "BillRefNumber",
    #         "MSISDN",
    #         "FirstName",
    #         "MiddleName",
    #         "LastName",
    #     ]
    # ) <= set(json_obj.keys()):
    #     return
    transaction = {}
    dt = json_obj["TransTime"]
    if json_obj["BillRefNumber"]:
        transaction["my_account"] = {
            "paybill_number": json_obj["BusinessShortCode"],
            "account_number": json_obj["BillRefNumber"],
        }
    else:
        transaction["my_account"] = {
            "till_number": json_obj["BusinessShortCode"],
        }
    transaction |= {
        "transaction_reference": json_obj["TransID"],
        "amount": convert_to_cash(json_obj["TransAmount"]),
        "initiated_at": isoparse(dt[:8] + "T" + dt[8:]),
        "other_account": {
            "account_name": " ".join(
                [
                    json_obj["FirstName"],
                    json_obj["MiddleName"],
                    json_obj["LastName"],
                ]
            ),
            "maybe_number": json_obj["MSISDN"],
        },
    }
    return transaction
