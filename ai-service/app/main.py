"""
AI Service entrypoint.

Loads the Whisper model once at startup (via the lifespan context
manager) so requests never pay the model-loading cost.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routes import transcribe, translate, synthesize, audio_pipeline, languages
from app.services import whisper_service, translation_service, speech_service
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup — load all models once, in sequence
    logger.info("Starting AI service — loading models...")
    whisper_service.load_model()
    translation_service.load_model()
    speech_service.load_model()
    logger.info("AI service ready.")
    yield
    # Shutdown
    logger.info("Shutting down AI service.")


app = FastAPI(
    title="Multilingual AI Platform — AI Service",
    description="Speech-to-text, translation, and speech generation microservice.",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(transcribe.router)
app.include_router(translate.router)
app.include_router(synthesize.router)
app.include_router(audio_pipeline.router)
app.include_router(languages.router)


@app.get("/health", tags=["Health"])
async def health():
    return {
        "status": "ok",
        "whisper_loaded": whisper_service.is_model_loaded(),
        "nllb_loaded": translation_service.is_model_loaded(),
        "seamless_loaded": speech_service.is_model_loaded(),
    }
