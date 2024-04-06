from pesarifu.etl.safaricom.tasks import process, setup
from pesarifu.util.tasks import email_report, generate_report, rebuild_report


def go(pdf_path, metadata, pdf_type):
    # TODO: figure out more effective method to share session
    chain = (
        setup.s(metadata["email"], pdf_path)
        | process.s(pdf_path, pdf_type)
        | generate_report.s()
        | rebuild_report.s()
        | email_report.s([".csv", ".xlsx"])
    )
    chain()
