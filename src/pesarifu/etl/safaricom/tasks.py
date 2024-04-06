from typing import Any

from sqlalchemy.orm import Session

from pesarifu.config.celery import app
from pesarifu.config.config import settings
from pesarifu.db.load import (
    get_account,
    get_or_create_account,
    get_or_create_user,
)
from pesarifu.db.util import db_connector
from pesarifu.etl.safaricom.extract import (
    get_metadata_from_pdf,
    get_transactions_from_pdf,
)
from pesarifu.etl.safaricom.load import (
    create_transaction,
    get_or_create_provider,
)
from pesarifu.etl.safaricom.transform import transform_pdf_record
from pesarifu.util.helpers import logger


@app.task(name=f"{__name__}.debug_connection")
def debug_connection():
    logger.info(f"DB url is {settings.DB_URL}")
    return settings.DB_URL


@app.task(name=f"{__name__}.setup")
@db_connector
def setup(session: Session, email: str, pdf_path: str) -> int:
    pdf_type, metadata = get_metadata_from_pdf(pdf_path)
    uinfo = {
        "email": email,
        "username": metadata["customer_name"],
        "phone_number": metadata["mobile_number"],
    }
    user = get_or_create_user(session, uinfo)
    provider = get_or_create_provider(session)

    mobile_obj = {
        "account_name": metadata["customer_name"],
        "maybe_number": metadata["mobile_number"],
    }
    tacc = get_or_create_account(session, mobile_obj, provider)
    tacc.holder = user
    session.commit()
    tid = tacc.id
    return tid


@app.task(name=f"{__name__}.process")
@db_connector
def process(
    session: Session, trans_account_id: int, pdf_path: str, pdf_type: int
):
    records = get_transactions_from_pdf(pdf_path, pdf_type=pdf_type)
    transformed_records = map(transform_pdf_record, records)
    trans_account = get_account(session, trans_account_id)
    ids = []
    logger.info(session)
    for rec in transformed_records:
        if rec:
            tx_id = create_transaction(session, trans_account, rec)
            ids.append(tx_id)
    return {"account_id": trans_account.id, "transaction_ids": ids}
