from fastapi import APIRouter, UploadFile, File
from app.supabase_client import supabase
import os

router = APIRouter()
BUCKET_NAME = "products"

@router.post("/upload")
async def upload_product(file: UploadFile = File(...)):
    contents = await file.read()
    supabase.storage.from_("products").upload(file.filename, contents)
    return {"filename": file.filename}

@router.get("/")
async def list_products():
    response = supabase.storage.from_("products").list()
    filenames = [item["name"] for item in response]
    return {"files": filenames}
