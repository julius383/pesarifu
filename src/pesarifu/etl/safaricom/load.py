from time import time
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from pesarifu.db.load import get_or_create_account
from pesarifu.db.models import Provider, Transaction, TransactionalAccount
from pesarifu.util.helpers import logger


def get_or_create_provider(session):
    obj = session.scalars(
        select(Provider).where(Provider.name == "Safaricom")
    ).first()
    if obj:
        return obj
    else:
        obj = Provider(name="Safaricom")
        session.add(obj)
        return obj


def create_transaction(
    session,
    account: TransactionalAccount | int,
    transaction: dict[str, Any],
):
    # print(transaction)
    other_account = transaction.pop("other_account")
    provider = get_or_create_provider(session)
    other = get_or_create_account(session, other_account, provider=provider)
    session.commit()
    tx_id = session.scalars(
        insert(Transaction)
        .returning(Transaction.id)
        .values(
            **transaction,
            owner_account_id=account.id,
            participant_account_id=other.id,
        )
        .on_conflict_do_update(
            constraint="transaction_unique_constraint",
            set_=dict(updated_at=(time())),
        )
    ).one()
    session.commit()
    return tx_id
