from pydantic import BaseModel, Field


class SynthesizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to convert to speech.")
    target_lang: str = Field(..., description="Target language code, e.g. 'hi'.")

    class Config:
        json_schema_extra = {
            "example": {
                "text": "आप कैसे हैं?",
                "target_lang": "hi",
            }
        }
