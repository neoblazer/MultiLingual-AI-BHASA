"""
Centralized supported-language definitions.

NLLB and SeamlessM4T use different language code schemes (NLLB uses
FLORES-200 codes like 'eng_Latn', 'hin_Deva'; SeamlessM4T uses its own
short codes like 'eng', 'hin'). Keeping the mapping here means routes
and services don't need to know these details — they just deal in
simple ISO-ish codes like 'en', 'hi' and this module translates.
"""

# Simple code -> NLLB FLORES-200 code
NLLB_LANG_MAP = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "fr": "fra_Latn",
    "es": "spa_Latn",
    "de": "deu_Latn",
    "ar": "arb_Arab",
    "zh": "zho_Hans",
    "ja": "jpn_Jpan",
    "ru": "rus_Cyrl",
    "pt": "por_Latn",
}

# Simple code -> SeamlessM4T language code
SEAMLESS_LANG_MAP = {
    "en": "eng",
    "hi": "hin",
    "fr": "fra",
    "es": "spa",
    "de": "deu",
    "ar": "arb",
    "zh": "cmn",
    "ja": "jpn",
    "ru": "rus",
    "pt": "por",
}


def is_supported_language(code: str) -> bool:
    return code in NLLB_LANG_MAP


def to_nllb_code(code: str) -> str:
    if code not in NLLB_LANG_MAP:
        raise ValueError(f"Unsupported language code for translation: '{code}'")
    return NLLB_LANG_MAP[code]


def to_seamless_code(code: str) -> str:
    if code not in SEAMLESS_LANG_MAP:
        raise ValueError(f"Unsupported language code for speech generation: '{code}'")
    return SEAMLESS_LANG_MAP[code]


def supported_languages() -> list:
    return sorted(NLLB_LANG_MAP.keys())
