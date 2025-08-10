from fastapi import APIRouter

default_router = APIRouter()


@default_router.get("/")
async def root():
    return {"message": "Welcome to the Moov API!"}
