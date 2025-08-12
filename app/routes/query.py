# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional
# from app.services.rag_service import query_rag  # Import from your local rag_service.py

# router = APIRouter()

# class QueryRequest(BaseModel):
#     query: str
#     top_k: Optional[int] = 3  # number of docs to retrieve

# @router.post("/query")
# async def query_endpoint(request: QueryRequest):
#     try:
#         response = query_rag(request.query, top_k=request.top_k)
#         return {"results": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3

@router.post("/query")
async def query_endpoint(request: QueryRequest):
    try:
        # Replace these IDs with actual values from request or auth
        response = rag_service.search(
            query=request.query,
            user_id="default_user",
            product_id="default_product"
        )
        return {"results": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

