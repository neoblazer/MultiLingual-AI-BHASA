from pydantic import BaseModel, Field
from typing import Optional


class AudioTranslateResponse(BaseModel):
    transcript: str
    source_language: Optional[str]
    translated_text: str
    translated_audio_url: str = Field(
        ..., description="Path/URL the caller can use to fetch the generated audio."
    )
