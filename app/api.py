from fastapi import APIRouter
from fastapi.responses import JSONResponse

api = APIRouter()

V1 = APIRouter(prefix="/v1")

@V1.get("/hello")
async def hello():
    return JSONResponse(
        status_code=200,
        content={"message": "hello world"}
    )

api.include_router(V1)