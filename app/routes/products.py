from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_products():
    return [{"id": 1, "name": "Product A"}, {"id": 2, "name": "Product B"}]

