from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from app.schemas.speech import SynthesizeRequest
from app.services import speech_service
from app.utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["Speech Generation"])


@router.post("/synthesize")
async def synthesize(payload: SynthesizeRequest):
    try:
        output_path = speech_service.synthesize_speech(payload.text, payload.target_lang)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Speech generation model is not ready yet.",
        ) from exc
    except Exception as exc:
        logger.exception("Speech synthesis failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate speech due to an internal error.",
        ) from exc

    return FileResponse(output_path, media_type="audio/wav", filename="translated_audio.wav")
