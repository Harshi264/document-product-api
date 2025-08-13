from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.rag_service import RAGService
import shutil
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Create a single RAGService instance
rag_service = RAGService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the class method (use the correct parameters your RAGService expects)
        rag_service._ingest_document(file_path, user_id="default_user", product_id="default_product")

        return {"status": "success", "filename": file.filename}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
