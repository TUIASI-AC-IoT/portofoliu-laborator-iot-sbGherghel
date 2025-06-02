from fastapi import FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from app.file_manager import FileManager

app = FastAPI()
file_manager = FileManager()


# Models
class FileContent(BaseModel):
    content: str


class FileCreate(FileContent):
    filename: str | None = None


class FileResponse(BaseModel):
    filename: str
    content: str


# Endpoints
@app.get("/files", response_model=list[str], summary="List all files")
def list_files():
    """List all files in the directory"""
    return file_manager.list_files()


@app.get("/files/{filename}", response_model=FileResponse, summary="Get file content")
def read_file(filename: str):
    """Get content of a specific file"""
    try:
        content = file_manager.read_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/files", response_model=FileResponse, status_code=201, summary="Create a file")
def create_file(file_data: FileCreate):
    """Create a new file with specified or generated name"""
    try:
        filename = file_manager.create_file(file_data.filename, file_data.content)
        content = file_manager.read_file(filename)
        return {"filename": filename, "content": content}
    except FileExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.put("/files/{filename}", response_model=FileResponse, summary="Update file content")
def update_file(filename: str, file_data: FileContent):
    """Update content of an existing file"""
    try:
        file_manager.update_file(filename, file_data.content)
        content = file_manager.read_file(filename)
        return {"filename": filename, "content": content}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.delete("/files/{filename}", status_code=204, summary="Delete a file")
def delete_file(filename: str):
    """Delete a file"""
    try:
        file_manager.delete_file(filename)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


# Custom OpenAPI schema
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="File Manager API",
        version="1.0.0",
        description="A simple RESTful service for managing files in a directory",
        routes=app.routes,
    )

    # Add more details to the schema if needed
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi