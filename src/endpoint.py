import os
import json
import requests
from base64 import b85encode
from time import time

from multipart import MultipartParser
from multipart.exceptions import MultipartParseError
from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse, JSONResponse

from .constants import WEBHOOK
from .download import download_chunk_data, iterfile
from .my_multipart import UploadFileByStream


router = APIRouter()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/download/{file_id}")
def download(file_id):
    futures, name = download_chunk_data(file_id)
    return StreamingResponse(iterfile(futures), headers={"Content-Disposition": f"attachment; filename={name}"})


@router.post("/upload")
async def upload_test(request: Request):
    start = time()
    filename = request.headers.get("file", None)

    content_type = request.headers.get("Content-Type")
    if not content_type or "boundary=" not in content_type:
        return JSONResponse(content="Invalid Content-Type header", status_code=400)

    _, boundary = content_type.split("boundary=")

    file = UploadFileByStream()

    callbacks = {
        'on_part_begin': file.on_part_begin,
        'on_part_data': file.on_part_data,
        'on_part_end': file.on_part_end,
        "on_header_value": file.on_header_value,
    }

    parser = MultipartParser(boundary, callbacks)
    async for chunk in request.stream():
        try:
            parser.write(chunk)
        except MultipartParseError as e:
            return JSONResponse(content=f"Invalid multipart data: {e}", status_code=400)

    file.collect_urls()

    if not file.urls:
        return JSONResponse(content="No file uploaded", status_code=400)

    if filename is None:
        filename = file.filename
    else:
        filename = "unknown.something"

    data = {
        "name": os.path.basename(filename),
        "id": file.urls,
    }
    response = requests.post(next(WEBHOOK), files={
        'file[0]': ('data', bytes(json.dumps(data), 'utf-8'))
    })
    response.raise_for_status()
    url = "/".join(response.json().get("attachments", [])[0]
                   ["url"].split("attachments/")[1].split("/")[:2])
    print(f"Uploaded {len(file.urls)} chunks in {time() - start} seconds")
    return {"id": b85encode(url.encode("utf-8")).hex()}
