"""
Combined pipeline route: Audio -> Whisper -> NLLB -> SeamlessM4T -> Translated Audio.

Internally this simply calls the three existing services in sequence —
it does NOT contain its own inference logic. Kept as a separate
endpoint from the individual ones per the SOP so callers can either
do the full pipeline in one call, or use each stage independently.
"""
import os
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import FileResponse
from app.schemas.pipeline import AudioTranslateResponse
from app.services import whisper_service, translation_service, speech_service
from app.utils.file_utils import validate_audio_file, save_upload_to_temp, cleanup_temp_file
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()
router = APIRouter(prefix="/api/audio", tags=["Audio Pipeline"])


@router.post("/translate", response_model=AudioTranslateResponse)
async def translate_audio(
    file: UploadFile = File(..., description="Source audio file"),
    target_lang: str = Form(..., description="Target language code, e.g. 'en'"),
):
    validate_audio_file(file)
    temp_input_path = save_upload_to_temp(file)

    try:
        # Stage 1: Whisper
        try:
            transcription = whisper_service.transcribe_audio(temp_input_path)
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Transcription model is not ready yet.",
            ) from exc

        transcript = transcription["transcript"]
        source_lang = transcription["detected_language"]

        if not transcript:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Could not extract any speech from the provided audio.",
            )

        # Stage 2: NLLB
        try:
            translated_text = translation_service.translate_text(
                transcript, source_lang, target_lang
            )
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Translation model is not ready yet.",
            ) from exc

        # Stage 3: SeamlessM4T
        try:
            output_audio_path = speech_service.synthesize_speech(translated_text, target_lang)
        except ValueError as exc:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
        except RuntimeError as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Speech generation model is not ready yet.",
            ) from exc

    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Audio translation pipeline failed")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Audio translation pipeline failed due to an internal error.",
        ) from exc
    finally:
        cleanup_temp_file(temp_input_path)

    filename = os.path.basename(output_audio_path)

    return AudioTranslateResponse(
        transcript=transcript,
        source_language=source_lang,
        translated_text=translated_text,
        translated_audio_url=f"/api/audio/output/{filename}",
    )


@router.get("/output/{filename}")
async def get_generated_audio(filename: str):
    """
    Serves a previously generated translated-audio file by name.
    Basic path traversal guard: reject anything containing path separators.
    """
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid filename.")

    file_path = os.path.join(settings.TEMP_OUTPUT_AUDIO_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Audio file not found.")

    return FileResponse(file_path, media_type="audio/wav", filename=filename)
