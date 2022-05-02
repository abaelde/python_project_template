import io
import os
import pathlib
import shutil
import uuid

from app.config import Settings, get_settings
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, StreamingResponse

router = APIRouter()


@router.get("/hello")
async def hello(settings: Settings = Depends(get_settings)):
    """Basic route to check that everything works

    Args:
        settings (Settings, optional): the fastapi setting.
        Defaults to Depends(get_settings).

    Returns:
        json: message to show that everythig works
    """
    return {
        "Hello": "World",
        "environment": settings.environment,
        "testing": settings.testing,
    }


@router.post("/hello-upload")
async def hello_upload(
    upload_file: UploadFile = File(...), settings: Settings = Depends(get_settings)
):
    """Route to test that we can upload a file

    Args:
        upload_file (UploadFile, optional): the file to upload. docx or pdf
        Defaults to File(...).

    Returns:
        json : success message
    """

    filename = upload_file.filename
    ext = os.path.splitext(filename)[1]
    if ext not in [".pdf", ".docx"]:
        raise HTTPException(status_code=400, detail="Extension must be pdf or docx")

    new_name = str(uuid.uuid4()) + ext

    saved_path = pathlib.Path(settings.uploads_folder) / new_name

    with open(saved_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {"msg": "upload is a success"}, 200


@router.get("/hello-download")
async def hello_download(settings: Settings = Depends(get_settings)):
    """Route to test that we can download a file.

    Downloads the first file in the uploads folder

    Args:
        upload_file (UploadFile, optional): the file to upload. docx or pdf
        Defaults to File(...).

    Returns:
        the first file
    """

    uploads_folder = pathlib.Path(settings.uploads_folder)
    pdf_docx_list = [
        file
        for file in list(uploads_folder.glob("*"))
        if file.suffix in [".pdf", ".docx"]
    ]

    if not pdf_docx_list:
        raise HTTPException(status_code=404, detail="No pdf or docx in uploads folder")
    else:
        returned_file = pdf_docx_list[0]
        if returned_file.suffix == ".pdf":
            media_type = "application/pdf"
        elif returned_file.suffix == ".docx":
            media_type = "application/vnd.openxmlformats-officedocument\
            .wordprocessingml.document"

    return FileResponse(pdf_docx_list[0], media_type=media_type)


@router.post("/hello-stream")
async def hello_stream(stream_file: UploadFile = File(...)):
    """Route to test that we can stream a file

    Args:
        stream_file (UploadFile, optional): the file to upload. docx or pdf
        Defaults to File(...).

    Returns:
        the same file
    """

    filename = stream_file.filename
    ext = os.path.splitext(filename)[1]

    if ext == ".pdf":
        media_type = "application/pdf"
    elif ext == ".docx":
        media_type = (
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        raise HTTPException(status_code=400, detail="Extension must be pdf or docx")

    contents = await stream_file.read()
    return_data = io.BytesIO()
    return_data.write(contents)
    return_data.seek(0)
    return StreamingResponse(return_data, media_type=media_type)
