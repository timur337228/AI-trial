import os

from fastapi import APIRouter, Depends, Header, status, Path, Query, Request, HTTPException, Response, UploadFile, File
from fastapi.staticfiles import StaticFiles
import aiofiles
from starlette.responses import StreamingResponse

from backend.api.ai.get_output_ai import get_completion, get_completion_stream
from backend.api.ai.scan import pdf_to_text
from backend.api.auth.validations import validate_auth_user, get_current_active_auth_user
from backend.api.models.models import User
from backend.config import BASE_DIR

prefix = "/ai"

router = APIRouter(prefix=prefix, tags=['ai'])

router.mount("/static", StaticFiles(directory=f"{BASE_DIR}/static"), name="static")


@router.post("/upload/")
async def upload_file(user: User = Depends(get_current_active_auth_user),
        file: UploadFile = File(...)):

    async with aiofiles.open(f"{BASE_DIR}/static/{user.email}.pdf", "wb") as f:
        content = await file.read()
        await f.write(content)
    text = pdf_to_text(f"{user.email}.pdf")
    async def generate():
        async for chunk in get_completion_stream(
                message=text,
        ):
            yield chunk

    return StreamingResponse(generate(), media_type="text/plain")
