from __future__ import annotations

import io
from pathlib import Path
from typing import Annotated, Optional

import sqlalchemy
from litestar import Litestar, Request, get, post
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.middleware.rate_limit import RateLimitConfig
from litestar.params import Body
from litestar.response import Template
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig
from pydantic import BaseModel, ConfigDict
from toolz import update_in

from pesarifu.config.config import settings
from pesarifu.db.models import ContactRequest
from pesarifu.db.util import Session
from pesarifu.etl import safaricom
from pesarifu.etl.safaricom.extract import get_metadata_from_pdf
from pesarifu.util.helpers import decrypt_pdf, format_timestamp, logger

# from icecream import ic


class ProcessItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sendto_email: str
    pdf_password: Optional[str] = None
    target: UploadFile
    source: str = "mpesa-full-statement"


class ContactForm(BaseModel):
    name: str
    message: str
    reason: Optional[str] = "General Enquiry"
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None


@get("/")
async def index() -> Template:
    context = {}
    context["api_url"] = settings.APP_BASE_URL
    return Template(template_name="index.html", context=context)


# TODO: add logic to register business with daraja callback endpoint
@post("/callback/register")
async def callback_register():
    return


@get("/test-success")
async def test_success() -> Template:
    t = Template(
        template_name="success.html",
        context={
            "customer_name": "John Smith",
            "email": "johnsmith@example.org",
            "mobile_number": "+254 700000000",
            "date_of_statement": 1690405200.0,
            "statement_period": {
                "start_ts": format_timestamp(1677618000.0),
                "end_ts": format_timestamp(1690405200.0),
            },
            "app_home": settings.APP_BASE_URL,
        },
    )
    return t


@get("/test-error")
async def test_error() -> Template:
    t = Template(
        template_name="error.html",
        context={
            "reason": "PDF type is not supported",
            "app_home": settings.APP_BASE_URL,
        },
    )
    return t


@post("/contact-us", exclude_from_csrf=True)
async def contact_us(data: ContactForm) -> str:
    session = Session()
    try:
        logger.info(
            "Received contact request",
            requested=data.name,
            contact=(data.contact_email or data.contact_phone),
        )
        session.add(ContactRequest(**data.model_dump(mode="python")))
    except sqlalchemy.exc.SQLAlchemyError:
        logger.exception("Could not save request", request=data)
    else:
        session.commit()
    finally:
        session.expunge_all()
        session.close()
    return "Request Submitted"


# TODO: add logic to handle PDFs from multiple sources safaricom, stanchart etc
@post("/process-pdf")
async def process_pdf(
    data: Annotated[
        ProcessItem, Body(media_type=RequestEncodingType.MULTI_PART)
    ]
) -> Template:
    try:
        file_head = await data.target.read(4)
        # TODO: add additional check for file size
        if not file_head.startswith(
            bytes([0x25, 0x50, 0x44, 0x46])
        ):  # PDF magic number
            logger.error(
                "Non PDF file passed", magic_number=file_head.hex(":")
            )
            raise HTTPException(
                detail="The submitted file is not a PDF", status_code=400
            )
        pdf_path = decrypt_pdf(
            io.BytesIO(file_head + await data.target.read()), data.pdf_password
        )
        logger.info("Saved pdf to %s", pdf_path)
        pdf_type, metadata = get_metadata_from_pdf(pdf_path)
        metadata["email"] = data.sendto_email
        if data.source == "mpesa-full-statement":
            safaricom.go(
                pdf_path=str(pdf_path.absolute()),
                metadata=metadata,
                pdf_type=pdf_type,
            )
            # nothing(pdf_path=str(pdf_path.absolute()), metadata=metadata)
        else:
            raise NotImplementedError
        metadata = update_in(
            metadata, ["statement_period", "start_ts"], format_timestamp
        )
        metadata = update_in(
            metadata, ["statement_period", "end_ts"], format_timestamp
        )
        metadata |= {
            "app_home": settings.APP_BASE_URL,
        }
        return Template(template_name="success.html", context=metadata)
    except ValueError:
        logger.exception("Unable to parse PDF as type %s", data.source)
        return Template(
            template_name="error.html",
            context={
                "reason": "the type of PDF you submitted is not yet supported.",
                "app_home": settings.APP_BASE_URL,
            },
        )
    except KeyError:
        logger.exception("No password provided in request")
        return Template(
            template_name="error.html",
            context={
                "reason": "a password is required for an encrypted PDF file",
                "app_home": settings.APP_BASE_URL,
            },
        )
    except Exception:
        logger.exception("Unhandled exception occurred")
        return Template(
            template_name="error.html",
            context={
                "reason": """an unknown error occurred, the admin has already been notified.\
            Feel free to contact us directly with additional questions""",
                "app_home": settings.APP_BASE_URL,
            },
        )


async def before_request_handler(request: Request) -> Optional[dict[str, str]]:
    body = await request.body()
    headers = request.headers
    logger.debug(
        "Request received", body=body, body_type=type(body), headers=headers
    )
    return None


rate_limit_config = RateLimitConfig(rate_limit=("minute", 10))

app = Litestar(
    route_handlers=[index, contact_us, process_pdf],
    openapi_config=None,
    cors_config=CORSConfig(
        allow_origins=[settings.APP_BASE_URL, settings.WEBSITE_BASE_URL]
    ),
    compression_config=CompressionConfig(
        backend="gzip", gzip_compress_level=9
    ),
    # before_request=before_request_handler,
    template_config=TemplateConfig(
        directory=Path(__file__).parent.parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    middleware=[rate_limit_config.middleware],
    static_files_config=[
        StaticFilesConfig(directories=["static/dist"], path="/dist")
    ],
)
