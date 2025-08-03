from fastapi import APIRouter, UploadFile, File
from app.supabase_client import supabase
import os

router = APIRouter()
BUCKET_NAME = "documents"

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    contents = await file.read()
    supabase.storage.from_("documents").upload(file.filename, contents)
    return {"filename": file.filename}

@router.get("/")
async def list_documents():
    response = supabase.storage.from_("documents").list()
    filenames = [item["name"] for item in response]
    return {"files": filenames}
