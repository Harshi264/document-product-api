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
from pydantic import BaseModel
from app.supabase_client import supabase

router = APIRouter()
BUCKET_NAME = "products"

# ✅ Upload a new product file to Supabase Storage
@router.post("/upload")
async def upload_product(file: UploadFile = File(...)):
    contents = await file.read()
    try:
        supabase.storage.from_(BUCKET_NAME).upload(file.filename, contents)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ List all product files from Supabase Storage
@router.get("/files")
async def list_product_files():
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        filenames = [item["name"] for item in response]
        return {"files": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Replace an existing product file
@router.put("/files/{filename}")
async def update_product_file(filename: str, file: UploadFile = File(...)):
    try:
        # Remove the existing file first
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        # Upload the new one with the same name
        contents = await file.read()
        supabase.storage.from_(BUCKET_NAME).upload(filename, contents)
        return {"message": f"{filename} replaced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete a product file
@router.delete("/files/{filename}")
async def delete_product_file(filename: str):
    try:
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Product table model
class Product(BaseModel):
    id: str
    name: str
    description: str
    price: float
    image: str

# ✅ Add a product to the products table in Supabase DB
@router.post("/")
async def add_product(product: Product):
    try:
        result = supabase.table("products").insert(product.dict()).execute()
        # Supabase Python client v2 returns data/error differently
        if hasattr(result, "error") and result.error:
            raise Exception(result.error)
        return {"message": "Product added", "product": product.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# (OPTIONAL) ✅ List products from the products table instead of storage bucket
@router.get("/")
async def list_products():
    try:
        result = supabase.table("products").select("*").execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


