# AI Service — Day 1: Whisper Transcription

## Milestone
Audio file → Whisper → Transcript

## Setup

```bash
cd ai-service
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Note: `faster-whisper` will download the selected model (default:
`small`, ~500MB) from Hugging Face on first run. This requires
internet access once; after that it's cached locally.

## Run

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger UI: http://localhost:8000/docs

## Test

### Health check
```bash
curl http://localhost:8000/health
```

### Transcribe
```bash
curl -X POST "http://localhost:8000/api/transcribe" \
  -F "file=@/path/to/your/audio.wav"
```

Expected response:
```json
{
  "transcript": "...",
  "detected_language": "en",
  "duration_seconds": 4.5
}
```

## What's implemented
- FastAPI app with clean structure (routes / services / config / utils)
- Whisper model loaded once at startup, not per request
- Audio file validation (extension + size)
- Temp file storage with guaranteed cleanup
- Error handling for invalid files, oversized files, and model failures
- Configuration entirely via environment variables

## Not yet implemented (upcoming days)
- NLLB translation
- SeamlessM4T speech generation
- Spring Boot backend
- React frontend
