"""
Whisper speech-to-text service.

Design choice: we use `faster-whisper` (a CTranslate2 reimplementation
of Whisper) instead of OpenAI's original `openai-whisper` package.

Trade-off:
- faster-whisper: significantly faster and lower memory on CPU, supports
  int8 quantization, same model quality (it loads the same Whisper
  weights). Slightly less "batteries included" than the original repo.
- openai-whisper: simpler reference implementation, but noticeably
  slower on CPU, which matters since this is a 10-day project likely
  running without a dedicated GPU.

Recommendation: faster-whisper, for practical inference speed during
development and demo.

The model is loaded exactly once at process startup (via the
lifespan hook in main.py) and reused for every request — reloading a
Whisper model per request would make each call take tens of seconds
just for model loading.
"""
from typing import Optional
from faster_whisper import WhisperModel
from app.config.settings import get_settings
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

_model: Optional[WhisperModel] = None


def load_model() -> None:
    """
    Loads the Whisper model into memory. Called once at app startup.
    """
    global _model
    if _model is not None:
        logger.info("Whisper model already loaded, skipping reload.")
        return

    logger.info(
        f"Loading Whisper model '{settings.WHISPER_MODEL_SIZE}' "
        f"on device='{settings.WHISPER_DEVICE}' "
        f"compute_type='{settings.WHISPER_COMPUTE_TYPE}'..."
    )
    _model = WhisperModel(
        settings.WHISPER_MODEL_SIZE,
        device=settings.WHISPER_DEVICE,
        compute_type=settings.WHISPER_COMPUTE_TYPE,
    )
    logger.info("Whisper model loaded successfully.")


def is_model_loaded() -> bool:
    return _model is not None


def transcribe_audio(file_path: str) -> dict:
    """
    Runs Whisper transcription on an audio file already saved to disk.

    Returns a dict with transcript text, detected language, and audio
    duration. Raises RuntimeError if the model hasn't been loaded yet.
    """
    if _model is None:
        raise RuntimeError("Whisper model is not loaded. Call load_model() at startup.")

    segments, info = _model.transcribe(file_path, beam_size=5)

    # segments is a generator; consuming it here also lets us get the
    # final duration/text out of it in one pass.
    transcript_parts = [segment.text.strip() for segment in segments]
    transcript = " ".join(transcript_parts).strip()

    return {
        "transcript": transcript,
        "detected_language": info.language,
        "duration_seconds": round(info.duration, 2) if info.duration else None,
    }
