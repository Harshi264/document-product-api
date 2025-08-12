# # from dotenv import load_dotenv
# # load_dotenv()

# # from fastapi import FastAPI
# # from fastapi.middleware.cors import CORSMiddleware
# # from app.routes import products, documents, chat  # added chat

# # app = FastAPI()

# # # CORS: allow your widget origin (or '*' while testing)
# # origins = [
# #     "https://memoria-chat-widget-xw2z.vercel.app",  # widget on Vercel
# #     "http://localhost:3000",                        # local Next.js dev
# #     ""  # remove '' in production for tighter security
# # ]

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=origins,
# #     allow_credentials=True,
# #     allow_methods=["*"],  # allows all HTTP methods
# #     allow_headers=["*"],  # allows all HTTP headers
# # )

# # # Routers
# # app.include_router(products.router, prefix="/products")
# # app.include_router(documents.router, prefix="/documents")
# # app.include_router(chat.router, prefix="/chat")  # new chat route

# # @app.get("/")
# # def read_root():
# #     return {"message": "API is working"}


# import os
# from dotenv import load_dotenv
# load_dotenv()

# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes import products, documents, chat, query, ingestion  # added RAG routes

# app = FastAPI(title="Unified Backend with RAG")

# # CORS settings
# origins = [
#     "https://memoria-chat-widget-xw2z.vercel.app",  # widget on Vercel
#     "http://localhost:3000",                        # local Next.js dev
#     ""  # remove '' in production for tighter security
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],  # allows all HTTP methods
#     allow_headers=["*"],  # allows all HTTP headers
# )

# # Routers
# app.include_router(products.router, prefix="/products", tags=["Products"])
# app.include_router(documents.router, prefix="/documents", tags=["Documents"])
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])
# app.include_router(query.router, prefix="/rag", tags=["RAG Query"])
# app.include_router(ingestion.router, prefix="/rag", tags=["RAG Ingestion"])

# @app.get("/", tags=["Health Check"])
# def read_root():
#     return {"status": "ok", "message": "Unified API is running"}
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "app.main:app",
#         host="0.0.0.0",
#         port=int(os.environ.get("PORT", 8000))
#     )

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load env variables early
load_dotenv()

from app.routes import products, documents, chat, query, ingestion

app = FastAPI(title="Unified Backend with RAG")

# CORS
origins = [
    "https://memoria-chat-widget-xw2z.vercel.app",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(products.router, prefix="/products", tags=["Products"])
app.include_router(documents.router, prefix="/documents", tags=["Documents"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(query.router, prefix="/rag", tags=["RAG Query"])
app.include_router(ingestion.router, prefix="/rag", tags=["RAG Ingestion"])

@app.get("/", tags=["Health Check"])
def read_root():
    return {"status": "ok", "message": "Unified API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render provides PORT env var
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
