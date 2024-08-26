from fastapi import APIRouter

main_header_router = APIRouter()

@main_header_router.get("/menu/header/main")
def read_main_header():
    return {"menu": "Main header navigation"}
