# CORRECTED: src/app/api/documents.py (Compatible with older supabase-py)

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.supabase_client import supabase
import mimetypes

router = APIRouter()
BUCKET_NAME = "documents"

@router.post("/upload")
async def upload_document(
    productId: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        file_extension = mimetypes.guess_extension(file.content_type) or ".pdf"
        unique_filename = f"{productId}{file_extension}"
        contents = await file.read()

        # --- MODIFICATION ---
        # 1. Get the full list of all files in the bucket.
        all_files_list = supabase.storage.from_(BUCKET_NAME).list()
        # 2. Create a set of filenames for a quick existence check.
        existing_filenames = {item['name'] for item in all_files_list}

        # 3. Check if our unique filename is in the set.
        if unique_filename in existing_filenames:
            response = supabase.storage.from_(BUCKET_NAME).update(unique_filename, contents)
        else:
            response = supabase.storage.from_(BUCKET_NAME).upload(unique_filename, contents)

        return {"filename": unique_filename, "message": "Document uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/")
async def list_documents():
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        return [item["name"] for item in response]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{productId}")
async def delete_document(productId: str):
    try:
        # --- MODIFICATION ---
        # 1. Get the full list of files.
        all_files_list = supabase.storage.from_(BUCKET_NAME).list()
        
        # 2. Filter the list in Python to find files matching the productId.
        files_to_delete = [
            item['name'] for item in all_files_list if item['name'].startswith(f"{productId}.")
        ]
        
        if not files_to_delete:
            raise HTTPException(status_code=404, detail="Document for this product not found.")
        
        supabase.storage.from_(BUCKET_NAME).remove(files_to_delete)
        return {"message": f"Documents for product {productId} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
