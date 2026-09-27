"""
Request/response models for transcription.

We don't need a request schema here since the request is a multipart
file upload (handled directly by FastAPI's UploadFile), but the
response is modeled explicitly so the API contract is clear and
documented in Swagger.
"""
from pydantic import BaseModel, Field
from typing import Optional


class TranscriptionResponse(BaseModel):
    transcript: str = Field(..., description="The transcribed text.")
    detected_language: Optional[str] = Field(
        None, description="Language code detected by Whisper, e.g. 'en', 'hi'."
    )
    duration_seconds: Optional[float] = Field(
        None, description="Duration of the processed audio, in seconds."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "transcript": "नमस्ते, आप कैसे हैं?",
                "detected_language": "hi",
                "duration_seconds": 3.42,
            }
        }
