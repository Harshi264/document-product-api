from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_documents():
    return [{"filename": "doc1.pdf"}, {"filename": "doc2.pdf"}]

