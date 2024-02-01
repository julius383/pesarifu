from __future__ import annotations

import io
from pathlib import Path
from typing import Annotated, Optional

from litestar import Litestar, get, post
from litestar.config.compression import CompressionConfig
from litestar.config.cors import CORSConfig
from litestar.config.csrf import CSRFConfig
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Template
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig
from pydantic import BaseModel, ConfigDict
from toolz import update_in

from pesarifu.config.config import settings
from pesarifu.etl import safaricom
from pesarifu.etl.safaricom.extract import get_metadata_from_pdf
from pesarifu.util.helpers import decrypt_pdf, format_timestamp, logger, nothing

# from icecream import ic


class ProcessItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sendto_email: str
    pdf_password: Optional[str] = None
    target: UploadFile
    source: str = "mpesa-full-statement"


class ContactForm(BaseModel):
    name: str
    reason: str = "unsupported_filetype"
    decription: Optional[str] = None
    follow_up: Optional[str] = None


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
    try:
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
            },
        )
        return t
    except Exception as e:
        print(e)
        logger.error("Error occurred", error=e)


@get("/test-error")
async def test_error() -> Template:
    try:
        t = Template(
            template_name="error.html",
            context={
                "reason": "PDF type is not supported",
            },
        )
        return t
    except Exception as e:
        print(e)
        logger.error("Error occurred", error=e)


@post("/contact-us")
async def contact_us(
    data: Annotated[
        ContactForm, Body(media_type=RequestEncodingType.URL_ENCODED)
    ]
) -> str:
    return ""


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
            logger.error("Non PDF file passed")
            raise HTTPException(
                detail="The submitted file is not a PDF", status_code=400
            )
        pdf_path = decrypt_pdf(
            io.BytesIO(file_head + await data.target.read()), data.pdf_password
        )
        logger.info("Saved pdf to %s", pdf_path)
        metadata = get_metadata_from_pdf(pdf_path)
        metadata["email"] = data.sendto_email
        if data.source == "mpesa-full-statement":
            logger.info("Dispatching Task")
            # safaricom.go(pdf_path=str(pdf_path.absolute()), metadata=metadata)
            nothing(pdf_path=str(pdf_path.absolute()), metadata=metadata)
        else:
            raise NotImplementedError
        metadata = update_in(
            metadata, ["statement_period", "start_ts"], format_timestamp
        )
        metadata = update_in(
            metadata, ["statement_period", "end_ts"], format_timestamp
        )
        return Template(template_name="success.html", context=metadata)
    except ValueError as e:
        logger.error("Unable to parse PDF as type %s", data.source)
        raise HTTPException(
            detail="Could not parse PDF as indicated type", status_code=400
        ) from e
    except KeyError as e:
        logger.error("No password provided in request")
        raise HTTPException(
            detail="Password required for encrypted PDF", status_code=400
        ) from e
    except Exception as e:
        logger.error("An error occurred", error=e)
        raise e


app = Litestar(
    route_handlers=[index, contact_us, process_pdf, test_success, test_error],
    openapi_config=None,
    cors_config=CORSConfig(allow_origins=[settings.APP_BASE_URL]),
    csrf_config=CSRFConfig(secret=settings.CSRF_SECRET),
    compression_config=CompressionConfig(
        backend="gzip", gzip_compress_level=9
    ),
    template_config=TemplateConfig(
        directory=Path(__file__).parent.parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    static_files_config=[
        StaticFilesConfig(directories=["static/dist"], path="/dist")
    ],
)
