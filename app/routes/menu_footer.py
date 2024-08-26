from fastapi import APIRouter

footer_router = APIRouter()

@footer_router.get("/menu/footer")
def read_footer():
    return {"menu": "Footer navigation links"}
