"""
Route layer for transcription.

Keeps HTTP concerns (file upload handling, status codes) separate from
inference logic, which lives in whisper_service.py.
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from app.schemas.transcription import TranscriptionResponse
from app.services import whisper_service
from app.utils.file_utils import validate_audio_file, save_upload_to_temp, cleanup_temp_file
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(prefix="/api", tags=["Transcription"])


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(..., description="Audio file to transcribe")):
    validate_audio_file(file)
    temp_path = save_upload_to_temp(file)

    try:
        result = whisper_service.transcribe_audio(temp_path)
    except RuntimeError as exc:
        logger.error(f"Whisper model not ready: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Transcription model is not ready yet. Please try again shortly.",
        ) from exc
    except Exception as exc:
        logger.exception("Transcription failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to transcribe audio due to an internal error.",
        ) from exc
    finally:
        cleanup_temp_file(temp_path)

    if not result["transcript"]:
        logger.warning("Transcription produced empty text.")

    return TranscriptionResponse(**result)
