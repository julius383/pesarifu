from __future__ import annotations
from typing import Annotated

from litestar import Litestar, get, post, MediaType
from litestar.datastructures import UploadFile
from litestar.enums import RequestEncodingType
from litestar.params import Body

from pydantic import BaseModel, ConfigDict

class ProcessItem(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    sendto: str
    target: UploadFile


@get("/")
async def hello_world() -> str:
    return "Hello, world!"


# TODO: add logic to include user id
@post("/callback/register")
async def callback_register():
    return


@post("/process-pdf", media_type=MediaType.TEXT)
async def process_pdf(data: Annotated[ProcessItem, Body(media_type=RequestEncodingType.MULTI_PART)]) -> str:
    content = await data.target.read()
    filename = data.target.filename
    return f"{data.sendto} {filename} {len(content)}"

app = Litestar(route_handlers=[hello_world, process_pdf])
