from time import time
from typing import Any

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from pesarifu.db.models import (
    MobileMoneyAccount,
    Provider,
    ProviderAccount,
    SafaricomBuygoodsAccount,
    SafaricomPaybillAccount,
    Transaction,
    TransactionalAccount,
    UserAccount,
)
from pesarifu.util.helpers import logger


def get_user(session, email=None, id_=None):
    if email:
        q = select(UserAccount).where(UserAccount.email == email)
    elif id_:
        q = select(UserAccount).where(UserAccount.id == id_)
    else:
        return None
    return session.scalars(q).first()


def get_account(session: Session, account_id: int) -> TransactionalAccount:
    return session.scalars(
        select(TransactionalAccount).where(
            TransactionalAccount.id == account_id
        )
    ).first()


def get_or_create_user(session, fields):
    obj = session.scalars(
        select(UserAccount).where(UserAccount.email == fields["email"])
    ).first()
    if obj:
        return obj
    else:
        obj = UserAccount(
            email=fields["email"], phone_number=fields["phone_number"]
        )
        session.add(obj)
        # session.commit()
        return obj


def get_or_create_account(session, obj, provider):
    if not isinstance(obj, dict):
        obj = obj.__dict__
    if "purpose" in obj:
        acc = session.scalars(
            select(ProviderAccount).where(
                ProviderAccount.account_name == "Safaricom"
            )
        ).first()
        if not acc:
            acc = ProviderAccount(
                account_name="Safaricom",
                provider=provider,
            )
            session.add(acc)

        return acc
    elif "maybe_number" in obj:
        # FIXME: handle assumption that all mobile accounts are from the same provider
        acc = session.scalars(
            select(MobileMoneyAccount)
            .where(MobileMoneyAccount.account_name == obj["account_name"])
            .where(MobileMoneyAccount.maybe_number == obj["maybe_number"])
        ).first()
        if not acc:
            acc = MobileMoneyAccount(
                account_name=obj["account_name"],
                maybe_number=obj["maybe_number"],
                provider=provider,
            )
            session.add(acc)

        return acc
    elif "paybill_number" in obj:
        acc = session.scalars(
            select(SafaricomPaybillAccount)
            .where(SafaricomPaybillAccount.account_name == obj["account_name"])
            .where(
                SafaricomPaybillAccount.paybill_number == obj["paybill_number"]
            )
        ).first()
        if not acc:
            acc = SafaricomPaybillAccount(
                account_name=obj["account_name"],
                paybill_number=obj["paybill_number"],
                account_number=obj["account_number"],
                provider=provider,
            )
            session.add(acc)
        return acc
    elif "buygoods_number" in obj:
        acc = session.scalars(
            select(SafaricomBuygoodsAccount)
            .where(
                SafaricomBuygoodsAccount.account_name == obj["account_name"]
            )
            .where(
                SafaricomBuygoodsAccount.buygoods_number
                == obj["buygoods_number"]
            )
        ).first()
        if not acc:
            acc = SafaricomBuygoodsAccount(
                account_name=obj["account_name"],
                buygoods_number=obj["buygoods_number"],
                provider=provider,
            )
            session.add(acc)
        return acc
    else:
        logger.error("account of unknown type found %s", obj)
        raise ValueError


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
