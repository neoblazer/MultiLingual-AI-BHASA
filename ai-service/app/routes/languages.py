from fastapi import APIRouter
from app.config.languages import supported_languages

router = APIRouter(prefix="/api", tags=["Metadata"])


@router.get("/languages")
async def get_supported_languages():
    return {"supported_languages": supported_languages()}
