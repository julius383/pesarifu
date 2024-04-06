import os
import re
from datetime import datetime, timezone
from enum import Enum, auto
from functools import reduce
from operator import or_
from typing import Dict, Optional

from dateutil.parser import isoparse
from icecream import ic
from lark import Lark, Token, Transformer, UnexpectedCharacters
from toolz import pipe

from pesarifu.util.helpers import ParseError, convert_to_cash, logger, omit

# TODO: align fields in JSON and PDF extract


class TransactionTypes(Enum):
    MOBILE_TRANSFER = auto()
    BUYGOODS_TRANSFER = auto()
    PAYBILL_TRANSFER = auto()
    SAFARICOM_TRANSFER = auto()


class DetailTransformer(Transformer):
    def detail(self, item):
        return item[0]

    def mobile_transfer(self, account_info):
        account_info = list(
            filter(lambda x: not isinstance(x, Token), account_info)
        )
        return reduce(or_, account_info)

    def buygoods(self, account_info):
        account_info = reduce(
            or_, list(filter(lambda x: not isinstance(x, Token), account_info))
        )
        d = omit(["business_number"], account_info)
        d["buygoods_number"] = account_info["business_number"]
        return d

    def paybill(self, account_info):
        account_info = reduce(
            or_, list(filter(lambda x: not isinstance(x, Token), account_info))
        )
        d = omit(["business_number"], account_info)
        d["paybill_number"] = account_info["business_number"]
        return d

    def business_number(self, item):
        item = item[0].value
        return {
            "business_number": pipe(
                item,
                str.strip,
            )
        }

    def account_number(self, item):
        item = item[0].value
        return {
            "account_number": pipe(
                item,
                str.strip,
            )
        }

    def extra_detail(self, item):
        item = item[0].value
        return {
            "extra": {
                "via": pipe(
                    item,
                    str.strip,
                )
            }
        }

    def reason(self, item):
        item = item[0].value
        return {
            "purpose": pipe(
                item,
                str.strip,
            )
        }

    def account_name(self, item):
        item = item[0].value
        return {
            "account_name": pipe(
                item,
                str.lower,
                lambda x: re.sub(
                    r"(?:^|\s)([a-zA-Z])",
                    lambda x: str.upper(x.group(0)),
                    x,
                ),  # Better Title Case than str.title
                lambda x: re.sub(r"null", "", x, re.IGNORECASE),
                str.strip,
            )
        }

    def maybe_number(self, item):
        item = item[0].value
        d = {}
        if not re.search(r"\*\*\*", item):
            d["phone_number"] = item
        d["maybe_number"] = pipe(
            item,
            str.strip,
            lambda x: re.sub(r"^0", "254", x),
            lambda x: re.sub(r"^7", "2547", x),
        )
        return d


def make_parser():
    with open(
        os.path.join(os.path.dirname(__file__), "details_grammar.ebnf"), "r"
    ) as fp:
        grammar = fp.read()
        parser = Lark(grammar, start="detail")
    return parser


def parse_details(details):
    parser = make_parser()
    t = DetailTransformer()
    r = t.transform(parser.parse(details))
    return r


# @save_results("~/code/Python/pesarifu-dev/pesarifu/details-parse")


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
    transaction["initiated_at"] = (
        transaction["initiated_at"].replace(tzinfo=timezone.utc).timestamp()
    )
    try:
        info = parse_details(record["details"])
    except UnexpectedCharacters:
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
