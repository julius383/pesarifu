from __future__ import annotations

import io
from pathlib import Path
from typing import Annotated, Any, Optional

from litestar import Litestar, get, post
from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.exceptions import HTTPException
from litestar.params import Body
from litestar.response import Template
from litestar.static_files.config import StaticFilesConfig
from litestar.template.config import TemplateConfig
from pydantic import BaseModel, ConfigDict

from pesarifu.config.constants import APP_BASE_URL
from pesarifu.etl import safaricom
from pesarifu.etl.safaricom.extract import get_metadata_from_pdf
from pesarifu.util.helpers import decrypt_pdf, logger

# from icecream import ic

# TODO: add security middleware and rate limiting


class ProcessItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sendto_email: str
    pdf_password: Optional[str] = None
    target: UploadFile
    source: str = "mpesa-full-statement"


@get("/")
async def index() -> Template:
    context = {}
    context["api_url"] = APP_BASE_URL
    return Template(template_name="index.html", context=context)


# TODO: add logic to include user id
@post("/callback/register")
async def callback_register():
    return


# TODO: add logic to handle PDFs from multiple sources safaricom, stanchart etc
@post("/process-pdf")
async def process_pdf(
    data: Annotated[
        ProcessItem, Body(media_type=RequestEncodingType.MULTI_PART)
    ]
) -> dict[str, Any]:
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
            safaricom.go(pdf_path=str(pdf_path.absolute()), metadata=metadata)
        else:
            raise NotImplementedError
        return metadata
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


app = Litestar(
    route_handlers=[index, process_pdf],
    template_config=TemplateConfig(
        directory=Path(__file__).parent.parent / "templates",
        engine=JinjaTemplateEngine,
    ),
    static_files_config=[
        StaticFilesConfig(directories=["static/dist"], path="/dist")
    ],
)
