from sqlalchemy.orm import Session

from pesarifu.config.celery import app
from pesarifu.etl.safaricom.extract import (
    get_metadata_from_pdf,
    get_transactions_from_pdf,
)
from pesarifu.etl.safaricom.load import (
    create_transaction,
    get_or_create_account,
    get_or_create_provider,
    get_or_create_user,
)
from pesarifu.etl.safaricom.transform import transform_pdf_record


@app.task(name=f"{__name__}.setup")
@db_connector
def setup(session: Session, email: str, pdf_path: str) -> int:
    metadata = get_metadata_from_pdf(pdf_path)
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
    tid = tacc.id
    session.commit()
    return tid


@app.task(name=f"{__name__}.process")
@db_connector
def process(session: Session, trans_account_id: int, pdf_path: Path):
    records = get_transactions_from_pdf(pdf_path)
    transformed_records = map(transform_pdf_record, records)
    ids = []
    for rec in transformed_records:
        if rec:
            tx_id = create_transaction(session, trans_account_id, rec)
            ids.append(tx_id)
    return {"account_id": trans_account_id, "transaction_ids": ids}


# TODO: add chain task that does both
