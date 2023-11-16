import os
import json
import requests
from base64 import b85encode, b85decode
from time import time
from concurrent.futures import ThreadPoolExecutor

from multipart import MultipartParser
from multipart.exceptions import MultipartParseError
from fastapi import Request, APIRouter
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.exceptions import HTTPException
import lz4.frame
import asyncio
import aiohttp

from .constants import WEBHOOK, WEBHOOK_LIST
from .my_multipart import UploadFileByStream
from .crypto import encrypt, decrypt

router = APIRouter()

@router.get("/ping")
def ping():
    return {"status": "pong"}


@router.get("/health")
def health():
    message = {}
    for webhook in WEBHOOK_LIST:
        status = requests.get(webhook).status_code
        if status != 200:
            message[webhook] = status
    return message or {"status": "ok"}


def iterfile(futures):
    for _, future in futures.items():
        result = future.result()
        yield result.content


@router.get("/download/{file_id}") # Blocking on multiple downloads request
async def download(file_id):
    try:
        file_id = b85decode(bytes.fromhex(file_id)).decode("utf-8")
    except Exception as e:
        print(e)
        return {"error": "Invalid file id."}

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://cdn.discordapp.com/attachments/{file_id}/data") as response:
            response.raise_for_status()

            try:
                data = json.loads(lz4.frame.decompress(decrypt(await response.read())))
            except ValueError as e:
                raise HTTPException(status_code=400, detail="Invalid file id.")

            executor = ThreadPoolExecutor()
            return StreamingResponse(
                iterfile({
                    i: executor.submit(
                        requests.get, f"https://cdn.discordapp.com/attachments/{url}/rip")
                    for i, url in enumerate(data["id"])
                }),
                media_type=data["mimetype"],
                headers={
                    "Content-Disposition": f"filename={data['name']}",
                    "Content-Length": str(data["size"]),
                    "X-filename": data["name"],
                }
            )


async def upload_to_webhook(encrypt_data):
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('file[0]', encrypt_data, filename='data')
        while True:
            try:
                async with session.post(next(WEBHOOK), data=data) as response:
                    response.raise_for_status()
                    json_data = await response.json()
                    url = "/".join(json_data.get("attachments", [])[0]
                                    ["url"].split("attachments/")[1].split("/")[:2])
                    return b85encode(url.encode("utf-8")).hex()
            except aiohttp.ClientError as e:
                print(f"upload_to_webhook| Client error occurred: {e}")
                continue


@router.post("/upload")
async def upload(request: Request):
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
        "on_header_field": file.on_header_field,
    }

    parser = MultipartParser(boundary, callbacks)

    async for chunk in request.stream():
        try:
            await asyncio.sleep(0)
            parser.write(chunk)
        except MultipartParseError as e:
            return JSONResponse(content=f"Invalid multipart data: {e}", status_code=400)
    await file.collect_urls()

    if not file.urls:
        return JSONResponse(content="No file uploaded", status_code=400)

    if filename is None:
        filename = file.filename
    else:
        filename = "unknown.something"

    data = {
        "name": os.path.basename(filename),
        "id": file.urls,
        "size": file.total_bytes,
        "mimetype": file.mimetype or "application/octet-stream",
    }
    compress_data = lz4.frame.compress(bytes(json.dumps(data), 'utf-8'))
    encrypt_data = encrypt(compress_data)

    url_hex = await upload_to_webhook(encrypt_data)
    print(f"Uploaded {len(file.urls)} chunks in {time() - start} seconds")
    return {"id": url_hex}
