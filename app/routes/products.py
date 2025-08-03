from fastapi import APIRouter, UploadFile, File
import os

router = APIRouter()
UPLOAD_DIR = "uploads/products"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_product(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}

@router.get("/")
async def list_products():
    return {"files": os.listdir(UPLOAD_DIR)}
