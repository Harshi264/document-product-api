from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routes import products, documents

app = FastAPI()

app.include_router(products.router, prefix="/products")
app.include_router(documents.router, prefix="/documents")

@app.get("/")
def read_root():
    return {"message": "API is working"}

