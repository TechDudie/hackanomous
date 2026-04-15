from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import config
from app.oauth import oauth

api = APIRouter()

V1 = APIRouter()
V1.include_router(oauth, prefix="/oauth")

@V1.get("/hello")
async def hello():
    return JSONResponse(
        status_code=200,
        content={"message": "hello world"}
    )

api.include_router(V1, prefix="/v1")