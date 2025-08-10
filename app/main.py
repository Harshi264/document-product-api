from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import products, documents, chat  # added chat

app = FastAPI()

# CORS: allow your widget origin (or '*' while testing)
origins = [
    "https://memoria-chat-widget-xw2z.vercel.app",  # widget on Vercel
    "http://localhost:3000",                        # local Next.js dev
    ""  # remove '' in production for tighter security
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # allows all HTTP methods
    allow_headers=["*"],  # allows all HTTP headers
)

# Routers
app.include_router(products.router, prefix="/products")
app.include_router(documents.router, prefix="/documents")
app.include_router(chat.router, prefix="/chat")  # new chat route

@app.get("/")
def read_root():
    return {"message": "API is working"}


