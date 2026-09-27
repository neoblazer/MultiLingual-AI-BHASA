from fastapi import APIRouter, HTTPException, status
from app.schemas.translation import TranslateRequest, TranslateResponse
from app.services import translation_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["Translation"])


@router.post("/translate", response_model=TranslateResponse)
async def translate(payload: TranslateRequest):
    try:
        translated = translation_service.translate_text(
            payload.text, payload.source_lang, payload.target_lang
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Translation model is not ready yet.",
        ) from exc
    except Exception as exc:
        logger.exception("Translation failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to translate text due to an internal error.",
        ) from exc

    return TranslateResponse(translated_text=translated)
