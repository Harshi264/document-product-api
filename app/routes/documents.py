# from fastapi import APIRouter, UploadFile, File
# from app.supabase_client import supabase
# import os

# router = APIRouter()
# BUCKET_NAME = "documents"

# @router.post("/upload")
# async def upload_document(file: UploadFile = File(...)):
#     contents = await file.read()
#     supabase.storage.from_("documents").upload(file.filename, contents)
#     return {"filename": file.filename}

# @router.get("/")
# async def list_documents():
#     response = supabase.storage.from_("documents").list()
#     filenames = [item["name"] for item in response]
#     return {"files": filenames}
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.supabase_client import supabase

router = APIRouter()
BUCKET_NAME = "documents"

# ✅ Upload a new document
@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        supabase.storage.from_(BUCKET_NAME).upload(file.filename, contents)
        return {"filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ List all document files
@router.get("/")
async def list_documents():
    try:
        response = supabase.storage.from_(BUCKET_NAME).list()
        filenames = [item["name"] for item in response]
        return {"files": filenames}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Replace (update) an existing document
@router.put("/{filename}")
async def update_document(filename: str, file: UploadFile = File(...)):
    try:
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        contents = await file.read()
        supabase.storage.from_(BUCKET_NAME).upload(filename, contents)
        return {"message": f"{filename} replaced successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Delete a document
@router.delete("/{filename}")
async def delete_document(filename: str):
    try:
        supabase.storage.from_(BUCKET_NAME).remove([filename])
        return {"message": f"{filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

