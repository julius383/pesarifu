import re

# TODO: write export for excel, csv and jsonl
# TODO: align fields in JSON and PDF extract

def parse_details(details: str):
    details = details.strip()
    details = re.sub(r"\s+|\\", " ", details)
    re_flags = re.IGNORECASE
    patterns = {
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
