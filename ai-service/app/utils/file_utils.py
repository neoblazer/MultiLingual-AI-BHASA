"""
Helpers for validating and temporarily storing uploaded audio files.

We never persist uploaded audio permanently — files are written to a
temp directory for the duration of processing and removed afterward.
"""
import os
import uuid
from fastapi import UploadFile, HTTPException, status
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()


def ensure_temp_dir() -> None:
    os.makedirs(settings.TEMP_AUDIO_DIR, exist_ok=True)


def validate_audio_file(file: UploadFile) -> None:
    """
    Basic validation: extension check. Size is checked while streaming
    to disk in save_upload_to_temp (so we never load an oversized file
    fully into memory first).
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided with uploaded audio.",
        )

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Unsupported audio format '{ext}'. "
                f"Allowed formats: {', '.join(settings.ALLOWED_AUDIO_EXTENSIONS)}"
            ),
        )


def save_upload_to_temp(file: UploadFile) -> str:
    """
    Streams the uploaded file to a temp path in chunks, enforcing the
    max size limit as it goes. Returns the temp file path.
    """
    ensure_temp_dir()
    ext = os.path.splitext(file.filename)[1].lower()
    temp_path = os.path.join(settings.TEMP_AUDIO_DIR, f"{uuid.uuid4().hex}{ext}")

    max_bytes = settings.MAX_AUDIO_FILE_SIZE_MB * 1024 * 1024
    total_written = 0
    chunk_size = 1024 * 1024  # 1 MB

    try:
        with open(temp_path, "wb") as out_file:
            while True:
                chunk = file.file.read(chunk_size)
                if not chunk:
                    break
                total_written += len(chunk)
                if total_written > max_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=(
                            f"Audio file exceeds max allowed size of "
                            f"{settings.MAX_AUDIO_FILE_SIZE_MB} MB."
                        ),
                    )
                out_file.write(chunk)
    except HTTPException:
        cleanup_temp_file(temp_path)
        raise
    except Exception as exc:
        cleanup_temp_file(temp_path)
        logger.exception("Failed to save uploaded audio to temp storage")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not read the uploaded audio file.",
        ) from exc

    if total_written == 0:
        cleanup_temp_file(temp_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded audio file is empty.",
        )

    return temp_path


def cleanup_temp_file(path: str) -> None:
    try:
        if path and os.path.exists(path):
            os.remove(path)
    except OSError:
        logger.warning(f"Failed to remove temp file: {path}")
