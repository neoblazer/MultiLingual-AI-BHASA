"""
SeamlessM4T speech generation (text -> speech) service.

Loaded once at startup. Kept isolated behind synthesize_speech() so a
dedicated TTS model could be substituted later without touching routes.
"""
import os
import uuid
import torch
import soundfile as sf
from transformers import AutoProcessor, SeamlessM4TForTextToSpeech
from app.config.settings import get_settings
from app.config.languages import to_seamless_code, is_supported_language
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

_model = None
_processor = None


def load_model() -> None:
    global _model, _processor
    if _model is not None:
        logger.info("SeamlessM4T model already loaded, skipping reload.")
        return

    logger.info(f"Loading SeamlessM4T model '{settings.SEAMLESS_MODEL_NAME}'...")
    _processor = AutoProcessor.from_pretrained(settings.SEAMLESS_MODEL_NAME)
    _model = SeamlessM4TForTextToSpeech.from_pretrained(settings.SEAMLESS_MODEL_NAME)
    _model.to(settings.SEAMLESS_DEVICE)
    _model.eval()
    logger.info("SeamlessM4T model loaded successfully.")


def is_model_loaded() -> bool:
    return _model is not None and _processor is not None


def synthesize_speech(text: str, target_lang: str) -> str:
    """
    Generates speech audio for `text` in `target_lang` (simple code,
    e.g. 'hi'). Saves the result as a temp .wav file and returns its
    path. Caller is responsible for cleanup once the file is served.
    """
    if _model is None or _processor is None:
        raise RuntimeError("SeamlessM4T model is not loaded. Call load_model() at startup.")

    if not text or not text.strip():
        raise ValueError("Text to synthesize must not be empty.")

    if not is_supported_language(target_lang):
        raise ValueError(f"Unsupported target language: '{target_lang}'")

    tgt_code = to_seamless_code(target_lang)

    inputs = _processor(text=text, src_lang=tgt_code, return_tensors="pt").to(settings.SEAMLESS_DEVICE)

    with torch.no_grad():
        audio_output = _model.generate(**inputs, tgt_lang=tgt_code)[0]

    os.makedirs(settings.TEMP_OUTPUT_AUDIO_DIR, exist_ok=True)
    output_path = os.path.join(
        settings.TEMP_OUTPUT_AUDIO_DIR, f"{uuid.uuid4().hex}.wav"
    )

    # SeamlessM4T's vocoder outputs audio at a fixed 16kHz regardless of
    # checkpoint. The config attribute name for this has proven
    # inconsistent across transformers versions, so we hardcode the
    # known, documented value here.
    sample_rate = 16000

    # audio_output shape is (1, num_samples) — soundfile expects a 1D
    # array (mono) or (num_samples, num_channels) for multi-channel.
    audio_array = audio_output.cpu().numpy().squeeze()
    sf.write(output_path, audio_array, samplerate=sample_rate)

    return output_path
