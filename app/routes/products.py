# from fastapi import APIRouter, UploadFile, File
# from app.supabase_client import supabase
# import os

# router = APIRouter()
# BUCKET_NAME = "products"

# @router.post("/upload")
# async def upload_product(file: UploadFile = File(...)):
#     contents = await file.read()
#     supabase.storage.from_("products").upload(file.filename, contents)
#     return {"filename": file.filename}

# @router.get("/")
# async def list_products():
#     response = supabase.storage.from_("products").list()
#     filenames = [item["name"] for item in response]
#     return {"files": filenames}
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.supabase_client import supabase

router = APIRouter()
BUCKET_NAME = "products"

# ✅ Upload a new product file
@router.post("/upload")
async def upload_product(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        supabase.storage.from_(BUCKET_NAME).upload(file.filename, contents)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ List all product files
@router.get("/")
async def list_products():
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        filenames = [item["name"] for item in response]
        return {"files": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Replace an existing product file
@router.put("/{filename}")
async def update_product(filename: str, file: UploadFile = File(...)):
    try:
        # Remove the existing file first
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        # Upload the new one with same name
        contents = await file.read()
        supabase.storage.from_(BUCKET_NAME).upload(filename, contents)
        return {"message": f"{filename} replaced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete a product file
@router.delete("/{filename}")
async def delete_product(filename: str):
    try:
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

