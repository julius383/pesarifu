import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import apprise
from apprise import NotifyFormat
from dotenv import dotenv_values

config = dotenv_values()

apobj = apprise.Apprise()
apobj.add(f"tgram://{config['TELEGRAM_BOT_TOKEN']}/6081822266", tag="admin")


def notify_admin(subject, body):
    title = f"Update on pesarifu regarding: {subject}"
    apobj.notify(
        title=title, body=body, tag="admin", body_format=NotifyFormat.MARKDOWN
    )
    return


def build_email(subject, body, from_, sendto, attachments):
    message = MIMEMultipart()
    message["From"] = from_
    message["To"] = sendto
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    if attachments:
        for path in attachments:
            path = Path(path) if isinstance(path, str) else path
            with open(path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attatchment; filename= {path.name}",
                )
                message.attach(part)
    return message.as_string()


def notify_user_email(subject, body, sendto, attatchments=None):
    from_ = config["MAIL_USER"]
    text = build_email(subject, body, from_, sendto, attatchments)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        "mail.privateemail.com", 465, context=context
    ) as server:
        server.login(from_, config["MAIL_PASS"])
        server.sendmail(from_, sendto, text)
