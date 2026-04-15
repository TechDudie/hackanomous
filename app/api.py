from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.config import config

api = APIRouter()

V1 = APIRouter(prefix="/v1")

@V1.get("/hello")
async def hello():
    return JSONResponse(
        status_code=200,
        content={"message": "hello world"}
    )

@V1.get("/test_config")
async def test_config():
    message = config.get("hackatime.oauth_secret", "six seven")
    return JSONResponse(
        status_code=200,
        content={"message": message}
    )

api.include_router(V1)