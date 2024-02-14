from functools import reduce
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin

from jinja2 import Environment, PackageLoader, select_autoescape
from sh import ErrorReturnCode, just
from sqlalchemy import select
from toolz import groupby

from pesarifu.config.celery import app
from pesarifu.config.config import settings
from pesarifu.db.models import WebReport
from pesarifu.db.util import db_connector
from pesarifu.etl.safaricom.load import get_account
from pesarifu.util.export import export_transactions
from pesarifu.util.helpers import cd, logger
from pesarifu.util.notify import notify_admin, notify_local, notify_user_email

env = Environment(
    loader=PackageLoader("pesarifu"), autoescape=select_autoescape()
)


@app.task
def email_report(report: dict[str, Any], filetypes=None):
    attachments = export_transactions(report["account_id"], filetypes)
    files = groupby(lambda x: Path(x).suffix, attachments)
    subject = f"Report for {report['account_name']}"

    template = env.get_template("email-report.html.jinja")
    body = template.render(files=files, report_link=report["link"])
    notify_user_email(subject, body, report["sendto"], attachments)
    return


@app.task
def notify_report(
    link: str,
    account_name: str,
    sendto: str,
    attachments: Optional[list] = None,
):
    subject = f"Report for {account_name}: {sendto}"
    notify_local(subject, f"{link}\n {' '.join(attachments)}")
    return


@app.task
def admin_report(subject, body):
    notify_admin(subject, body)
    return


@app.task
@db_connector
def generate_report(session, transaction_result):
    account = get_account(session, transaction_result["account_id"])
    rel_path = account.holder.uuid.hex
    report_path = reduce(
        urljoin, ["reports/", rel_path], settings.REPORTS_BASE_URL
    )
    logger.info("Generating report on path: %s", report_path)
    maybe_report = session.scalars(
        select(WebReport).where(WebReport.account_id == account.id)
    ).one_or_none()
    if maybe_report:
        report = maybe_report
    else:
        report = WebReport(web_url=report_path, account=account)
        session.add(report)
        session.commit()
    return {
        "account_id": account.id,
        "link": report_path,
        "account_name": account.account_name,
        "sendto": account.holder.email,
    }


# FIXME: figure out way to make sure only single instance is running
@app.task
def rebuild_report(report: dict[str, Any]):
    try:
        with cd(settings.APP_ROOT):
            just("reports-build")  # see justfile in project root
            logger.info("Finished rebuilding report")
    except ErrorReturnCode:
        logger.exception("Failed to rebuild evidence report")
    return report
