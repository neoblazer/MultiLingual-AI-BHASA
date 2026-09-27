"""
NLLB text-to-text translation service.

Loaded once at startup, same pattern as Whisper. Kept fully decoupled
from FastAPI routes — routes only ever call translate_text().

Design note: NLLB is accessed via Hugging Face Transformers'
AutoModelForSeq2SeqLM + AutoTokenizer, using the tokenizer's
forced_bos_token_id mechanism to specify the target language. This
keeps translation swappable later (per SOP requirement) — a different
model can be substituted here without changing the route or the
public translate_text() signature.
"""
from typing import Optional
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from app.config.settings import get_settings
from app.config.languages import to_nllb_code, is_supported_language
from app.utils.logger import get_logger

logger = get_logger(__name__)
settings = get_settings()

_model = None
_tokenizer = None


def load_model() -> None:
    global _model, _tokenizer
    if _model is not None:
        logger.info("NLLB model already loaded, skipping reload.")
        return

    logger.info(f"Loading NLLB model '{settings.NLLB_MODEL_NAME}'...")
    _tokenizer = AutoTokenizer.from_pretrained(settings.NLLB_MODEL_NAME)
    _model = AutoModelForSeq2SeqLM.from_pretrained(settings.NLLB_MODEL_NAME)
    _model.to(settings.NLLB_DEVICE)
    _model.eval()
    logger.info("NLLB model loaded successfully.")


def is_model_loaded() -> bool:
    return _model is not None and _tokenizer is not None


def translate_text(text: str, source_lang: str, target_lang: str) -> str:
    """
    Translates text from source_lang to target_lang (simple codes,
    e.g. 'en', 'hi' — mapped internally to NLLB FLORES-200 codes).
    """
    if _model is None or _tokenizer is None:
        raise RuntimeError("NLLB model is not loaded. Call load_model() at startup.")

    if not text or not text.strip():
        raise ValueError("Text to translate must not be empty.")

    if not is_supported_language(source_lang):
        raise ValueError(f"Unsupported source language: '{source_lang}'")
    if not is_supported_language(target_lang):
        raise ValueError(f"Unsupported target language: '{target_lang}'")

    src_code = to_nllb_code(source_lang)
    tgt_code = to_nllb_code(target_lang)

    _tokenizer.src_lang = src_code
    inputs = _tokenizer(text, return_tensors="pt", truncation=True,
                         max_length=settings.NLLB_MAX_LENGTH).to(settings.NLLB_DEVICE)

    forced_bos_token_id = _tokenizer.convert_tokens_to_ids(tgt_code)

    with torch.no_grad():
        generated_tokens = _model.generate(
            **inputs,
            forced_bos_token_id=forced_bos_token_id,
            max_length=settings.NLLB_MAX_LENGTH,
        )

    translated = _tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
    return translated.strip()
