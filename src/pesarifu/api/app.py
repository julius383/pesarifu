from __future__ import annotations
from typing import Annotated, Optional, Any
import io

from litestar import Litestar, get, post
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.exceptions import HTTPException

from pydantic import BaseModel, ConfigDict
# from icecream import ic

from pesarifu.util.helpers import decrypt_pdf, logger
from pesarifu.etl.safaricom.extract import get_metadata_from_pdf


class ProcessItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sendto_email: str
    pdf_password: Optional[str] = None
    target: UploadFile
    source: str = 'mpesa_full_statement'


@get("/")
async def hello_world() -> str:
    return "Hello, world!"


# TODO: add logic to include user id
@post("/callback/register")
async def callback_register():
    return


# TODO: pass task to celery (delete or process) pdf
# TODO: add logic to handle PDFs from multiple sources safaricom, stanchart etc
@post("/process-pdf")
async def process_pdf(
    data: Annotated[ProcessItem, Body(
        media_type=RequestEncodingType.MULTI_PART)]
) -> dict[str, Any]:
    try:
        pdf_path = decrypt_pdf(io.BytesIO(await data.target.read()), data.pdf_password)
        logger.info("Saved pdf to %s", pdf_path)
        metadata = get_metadata_from_pdf(pdf_path)
        return metadata
    except ValueError as e:
        logger.error("Unable to parse PDF as type %s", data.source)
        raise HTTPException(
            detail="Could not parse PDF as indicated type",
            status_code=400
        ) from e
    except KeyError as e:
        logger.error("No password provided in request")
        raise HTTPException(
            detail="Password required for encrypted PDF",
            status_code=400
        ) from e

app = Litestar(route_handlers=[hello_world, process_pdf])
