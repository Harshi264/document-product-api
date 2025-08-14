# from fastapi import APIRouter, UploadFile, File, HTTPException
# from app.supabase_client import supabase

# router = APIRouter()
# BUCKET_NAME = "documents"

# # ✅ Upload a new document
# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         supabase.storage.from_(BUCKET_NAME).upload(file.filename, contents)
#         return {"filename": file.filename}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ✅ List all document files
# @router.get("/")
# async def list_documents():
#     try:
#         response = supabase.storage.from_(BUCKET_NAME).list()
#         filenames = [item["name"] for item in response]
#         return {"files": filenames}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ✅ Replace (update) an existing document
# @router.put("/{filename}")
# async def update_document(filename: str, file: UploadFile = File(...)):
#     try:
#         supabase.storage.from_(BUCKET_NAME).remove([filename])
#         contents = await file.read()
#         supabase.storage.from_(BUCKET_NAME).upload(filename, contents)
#         return {"message": f"{filename} replaced successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# # ✅ Delete a document
# @router.delete("/{filename}")
# async def delete_document(filename: str):
#     try:
#         supabase.storage.from_(BUCKET_NAME).remove([filename])
#         return {"message": f"{filename} deleted successfully"}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# CORRECTED: src/app/api/documents.py

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.supabase_client import supabase
import mimetypes # Used to get the file extension

router = APIRouter()
BUCKET_NAME = "documents"

# ✅ 1. Accept 'productId' from the form data.
@router.post("/upload")
async def upload_document(
    productId: str = Form(...),
    file: UploadFile = File(...)
):
    try:
        # ✅ 2. Create a unique filename based on the productId.
        # This guarantees one unique document per product.
        # Example: 'prod_123.pdf'
        file_extension = mimetypes.guess_extension(file.content_type) or ".pdf"
        unique_filename = f"{productId}{file_extension}"

        contents = await file.read()

        # Check if file exists to decide whether to upload or update
        existing_files = supabase.storage.from_(BUCKET_NAME).list(path="", search=unique_filename)
        
        if existing_files:
            # If it exists, use update() which overwrites the file
            response = supabase.storage.from_(BUCKET_NAME).update(unique_filename, contents)
        else:
            # If it doesn't exist, use upload()
            response = supabase.storage.from_(BUCKET_NAME).upload(unique_filename, contents)

        return {"filename": unique_filename, "message": "Document uploaded successfully."}
    except Exception as e:
        # This will catch the actual error from Supabase if something goes wrong.
        raise HTTPException(status_code=409, detail=str(e))


# ✅ List all document files (no change needed here)
@router.get("/")
async def list_documents():
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        return [item["name"] for item in response]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ Delete a document using the product ID
@router.delete("/{productId}")
async def delete_document(productId: str):
    try:
        # To make this robust, find any file starting with the productId
        files_to_delete = supabase.storage.from_(BUCKET_NAME).list(path="", search=f"{productId}.")
        if not files_to_delete:
            raise HTTPException(status_code=404, detail="Document for this product not found.")
        
        filenames = [file['name'] for file in files_to_delete]
        supabase.storage.from_(BUCKET_NAME).remove(filenames)
        return {"message": f"Documents for product {productId} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))