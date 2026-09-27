"""
Application configuration.

All tunable values come from environment variables so nothing is
hard-coded (model names, ports, temp directories, etc.). Defaults are
provided for local development convenience only.
"""
import os
from functools import lru_cache


class Settings:
    # Whisper model settings
    WHISPER_MODEL_SIZE: str = os.getenv("WHISPER_MODEL_SIZE", "small")
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")  # "cpu" or "cuda"
    WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")

    # Temp file handling
    TEMP_AUDIO_DIR: str = os.getenv("TEMP_AUDIO_DIR", "/tmp/ai-service-audio")

    # File validation
    MAX_AUDIO_FILE_SIZE_MB: int = int(os.getenv("MAX_AUDIO_FILE_SIZE_MB", "25"))
    ALLOWED_AUDIO_EXTENSIONS: tuple = (".wav", ".mp3", ".m4a", ".flac", ".ogg", ".webm")

    # NLLB translation model
    NLLB_MODEL_NAME: str = os.getenv("NLLB_MODEL_NAME", "facebook/nllb-200-distilled-600M")
    NLLB_DEVICE: str = os.getenv("NLLB_DEVICE", "cpu")
    NLLB_MAX_LENGTH: int = int(os.getenv("NLLB_MAX_LENGTH", "512"))

    # SeamlessM4T speech generation model
    SEAMLESS_MODEL_NAME: str = os.getenv("SEAMLESS_MODEL_NAME", "facebook/hf-seamless-m4t-medium")
    SEAMLESS_DEVICE: str = os.getenv("SEAMLESS_DEVICE", "cpu")
    TEMP_OUTPUT_AUDIO_DIR: str = os.getenv("TEMP_OUTPUT_AUDIO_DIR", "/tmp/ai-service-audio-out")

    # Server
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance. lru_cache ensures we parse env vars once,
    not on every request that needs config.
    """
    return Settings()
