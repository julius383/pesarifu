from pesarifu.db.util import db_connector
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
from pesarifu.util.helpers import pick


@db_connector
def go(session, pdf_path, metadata):
    uinfo = pick(["email"], metadata)
    uinfo["username"] = metadata["customer_name"]
    uinfo["phone_number"] = metadata["mobile_number"]
    user = get_or_create_user(session, uinfo)

    provider = get_or_create_provider(session)

    mobile_obj = {
        "account_name": metadata["customer_name"],
        "maybe_number": metadata["mobile_number"],
    }
    uacc = get_or_create_account(session, mobile_obj, provider)
    uacc.holder = user

    records = get_transactions_from_pdf(pdf_path)
    txs = map(transform_pdf_record, records)
    for tx in txs:
        if tx:
            create_transaction(session, uacc, tx)
    return
