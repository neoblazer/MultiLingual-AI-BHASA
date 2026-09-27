from pydantic import BaseModel, Field


class TranslateRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Source text to translate.")
    source_lang: str = Field(..., description="Source language code, e.g. 'en'.")
    target_lang: str = Field(..., description="Target language code, e.g. 'hi'.")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "How are you?",
                "source_lang": "en",
                "target_lang": "hi",
            }
        }


class TranslateResponse(BaseModel):
    translated_text: str
