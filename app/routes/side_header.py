from fastapi import APIRouter

side_header_router = APIRouter()

@side_header_router.get("/menu/header/side")
def read_side_header():
    return {"menu": "Side header navigation for member-related"}
