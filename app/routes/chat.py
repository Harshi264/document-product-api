# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# from typing import Optional, List
# import os
# import io
# # import requests

# from app.supabase_client import supabase
# from openai import OpenAI

# # Init OpenAI client
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# router = APIRouter()

# class ChatQuery(BaseModel):
#     query: str
#     product_id: Optional[str] = None  # Optional but helps filter context

# def run_rag_query(user_query: str, product_id: Optional[str] = None) -> str:
#     """
#     Retrieves relevant document chunks from Supabase + Vector DB,
#     sends them to LLM, and returns the contextual answer.
#     """
#     try:
#         # --- Step 1: Get embedding for the query ---
#         embedding_response = client.embeddings.create(
#             model="text-embedding-3-small",
#             input=user_query
#         )
#         query_embedding = embedding_response.data[0].embedding

#         # --- Step 2: Search vector DB for similar chunks ---
#         # Example: Supabase RPC call if using pgvector
#         filters = {}
#         if product_id:
#             filters["product_id"] = product_id

#         # You need a "match_documents" RPC in Supabase that searches by embedding
#         match_res = supabase.rpc("match_documents", {
#             "query_embedding": query_embedding,
#             "match_count": 5,
#             **filters
#         }).execute()

#         if not match_res.data:
#             return "Sorry, I couldn't find relevant information."

#         # --- Step 3: Combine top chunks into a context string ---
#         context_chunks: List[str] = [item["content"] for item in match_res.data]
#         context_text = "\n\n".join(context_chunks)

#         # --- Step 4: Ask LLM with the context ---
#         prompt = f"""
#         You are a helpful assistant. Use ONLY the context below to answer the question.
#         If the answer is not in the context, say you don't know.

#         Context:
#         {context_text}

#         Question:
#         {user_query}
#         """

#         completion = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.2
#         )

#         answer = completion.choices[0].message["content"]
#         return answer.strip()

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"RAG pipeline error: {e}")

# @router.post("/query")
# async def query_chat(data: ChatQuery):
#     """
#     Receives a query (and optional product_id), runs it through RAG pipeline,
#     returns an answer from relevant PDF/document context.
#     """
#     try:
#         answer = run_rag_query(
#             user_query=data.query,
#             product_id=data.product_id
#         )
#         return {"answer": answer}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import os

from app.supabase_client import supabase
from openai import OpenAI

# Init OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

router = APIRouter()

class ChatQuery(BaseModel):
    question: str                     # ✅ Changed from 'query' to 'question'
    product_id: Optional[str] = None  # Optional but helps filter context

def run_rag_query(user_question: str, product_id: Optional[str] = None) -> str:
    """
    Retrieves relevant document chunks from Supabase + Vector DB,
    sends them to LLM, and returns the contextual answer.
    """
    try:
        # --- Step 1: Get embedding for the question ---
        embedding_response = client.embeddings.create(
            model="text-embedding-3-small",
            input=user_question
        )
        query_embedding = embedding_response.data[0].embedding

        # --- Step 2: Search vector DB for similar chunks ---
        filters = {}
        if product_id:
            filters["product_id"] = product_id

        # Example: pgvector RPC in Supabase
        match_res = supabase.rpc("match_documents", {
            "query_embedding": query_embedding,
            "match_count": 5,
            **filters
        }).execute()

        if not match_res.data:
            return "Sorry, I couldn't find relevant information."

        # --- Step 3: Combine top chunks into a context string ---
        context_chunks: List[str] = [item["content"] for item in match_res.data]
        context_text = "\n\n".join(context_chunks)

        # --- Step 4: Ask LLM with the context ---
        prompt = f"""
        You are a helpful assistant. Use ONLY the context below to answer the question.
        If the answer is not in the context, say you don't know.

        Context:
        {context_text}

        Question:
        {user_question}
        """

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )

        # OpenAI Python SDK v1 return format
        return completion.choices[0].message["content"].strip()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG pipeline error: {e}")

@router.post("/query")
async def query_chat(data: ChatQuery):
    """
    Receives a question (and optional product_id), runs it through RAG pipeline,
    returns an answer from relevant PDF/document context.
    """
    try:
        answer = run_rag_query(
            user_question=data.question,     # ✅ matches frontend body
            product_id=data.product_id
        )
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
