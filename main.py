from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

from src.endpoint import router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# set fastapi swagger information to: paths: /upload: post: summary: Uploads a file. consumes: - multipart/form-data parameters: - in: formData name: upfile type: file description: The file to upload.


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Upload API",
        version="0.0.1",
        description="Yoyo",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    file_multipart_component = {
        "Body_create_upload_file__post": {
            "title": "Body_create_upload_file__post",
            "type": "object",
            "properties": {
                    "file": {
                        "title": "File",
                        "type": "string",
                        "format": "binary"
                    }
            }
        }
    }
    openapi_schema["components"]["schemas"].update(file_multipart_component)
    upload_endpoint_data = {
        "requestBody": {
            "content": {
                "multipart/form-data": {
                    "schema": {
                        "$ref": "#/components/schemas/Body_create_upload_file__post"
                    }
                }
            }
        }
    }
    openapi_schema["paths"]["/upload"]["post"].update(upload_endpoint_data)
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
