# Bhāṣā — Multilingual AI Platform for Text and Audio Translation

A full-stack platform that translates text and speech between multiple languages, combining speech recognition, neural machine translation, and speech synthesis into a single pipeline.

## What it does

- **Text translation** — translate typed text between supported language pairs.
- **Audio transcription** — upload a voice recording and get a text transcript.
- **Audio translation** — upload a voice recording and get back a transcript, translated text, and translated audio, in one call.

## Pipeline

```
Audio Input
    │
    ▼
Whisper  (speech → text)
    │
    ▼
NLLB  (text → translated text)
    │
    ▼
SeamlessM4T  (translated text → speech)
    │
    ▼
Translated Audio
```

## Architecture

```
React Frontend  →  Spring Boot Backend  →  FastAPI AI Service  →  AI Models
   (port 3000)         (port 8080)             (port 8000)
```

- **React Frontend** — text/audio translation workspace, session history, placeholder auth UI.
- **Spring Boot Backend** — REST API, request validation, translation-history persistence (PostgreSQL). Never runs AI models directly; delegates every AI operation to the AI service over HTTP.
- **FastAPI AI Service** — loads Whisper, NLLB, and SeamlessM4T once at startup and exposes them as REST endpoints. Route → Service → Model layering throughout.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, React Router |
| Backend | Java 21, Spring Boot, Spring Data JPA, PostgreSQL |
| AI Service | Python, FastAPI, PyTorch, Hugging Face Transformers, faster-whisper |
| Models | Whisper (speech-to-text), NLLB (translation), SeamlessM4T (speech generation) |

## Project structure

```
.
├── ai-service/     Python FastAPI AI service (Whisper, NLLB, SeamlessM4T)
├── backend/        Java Spring Boot backend
├── frontend/       React frontend
└── .gitignore
```

Each folder has its own `README.md` with setup and run instructions specific to that service.

## Running the project

All three services run independently and must be started separately, in this order:

1. **AI service** (port 8000) — see `ai-service/README.md`
2. **Backend** (port 8080) — see `backend/README.md`, requires PostgreSQL and the AI service running
3. **Frontend** (port 3000) — see `frontend/README.md`, requires the backend running

## API overview

**AI Service**
| Endpoint | Description |
|---|---|
| `POST /api/transcribe` | Audio → transcript |
| `POST /api/translate` | Text → translated text |
| `POST /api/synthesize` | Text → generated audio |
| `POST /api/audio/translate` | Audio → transcript + translated text + translated audio |

**Backend**
| Endpoint | Description |
|---|---|
| `POST /api/text/translate` | Text translation (proxies AI service, persists history) |
| `POST /api/audio/transcribe` | Audio transcription (proxies AI service) |
| `POST /api/audio/translate` | Full audio translation pipeline (proxies AI service) |

## Scope

Deliberately excluded from this phase: authentication (Spring Security/JWT), RAG, vector databases, and video translation. These are documented future-scope items — see the "What's next" section in the frontend.

## Status

- Text translation and audio transcription: working reliably.
- Speech generation (SeamlessM4T): functional, output accuracy under continued refinement.

## Future scope

- Video translation (extract audio → translate → re-mux)
- Subtitle generation
- Real-time speech translation
- Speaker voice preservation
- Authentication (JWT-based login/register)
