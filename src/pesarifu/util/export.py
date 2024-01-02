from functools import partial
from pathlib import Path
from uuid import uuid4

import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import aliased

from pesarifu.db.models import Transaction, TransactionalAccount
from pesarifu.db.util import engine
from pesarifu.util.helpers import EXPORTS_BASE_DIR, logger

account_alias = aliased(TransactionalAccount)


def generate_file_stem():
    return uuid4().hex[:16]


def export_transactions(account_id, filetypes=(".csv",), path_stem=None):
    with engine.connect() as connection:
        q = (
            select(
                Transaction.transaction_reference,
                Transaction.amount,
                Transaction.initiated_at,
                Transaction.original_detail,
                account_alias.account_name,
            )
            .join(account_alias, Transaction.participant_account)
            .where(Transaction.owner_account_id == account_id)
            .order_by(Transaction.initiated_at)
        )
        df = pd.read_sql(q, connection, parse_dates=["initiated_at"])
        size, _ = df.shape
        path_stem = path_stem if path_stem else generate_file_stem()
        paths = []
        for filetype in filetypes:
            filename = Path(path_stem).with_suffix(filetype)
            path = EXPORTS_BASE_DIR / filename
            if size >= 1000:
                filename = filename.with_suffix(".zip")
            if filetype.endswith(".xlsx"):
                export = df.to_excel
            elif filetype.endswith(".json"):
                export = partial(
                    df.to_json, orient="records", date_format="iso"
                )
            elif filetype.endswith(".jsonl"):
                export = partial(
                    df.to_json, orient="records", lines=True, date_format="iso"
                )
            else:
                export = partial(
                    df.to_csv,
                    index_label="index",
                    columns=[
                        "transaction_reference",
                        "amount",
                        "initiated_at",
                        "original_detail",
                        "account_name",
                    ],
                )
            export(path)
            logger.info(
                f"Exported transactions for account: {account_id} to {path}"
            )
            paths.append(str(path.absolute()))
        return paths
