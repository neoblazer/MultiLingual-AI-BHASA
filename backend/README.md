# Backend — Spring Boot

## Prerequisites
- Java 21
- Maven
- PostgreSQL running locally (or update `application.yml` env vars)
- The AI service (FastAPI) running, since this backend calls it over HTTP

## Configuration

All configuration is via environment variables (see `application.yml` for defaults):

| Variable | Default | Purpose |
|---|---|---|
| `SERVER_PORT` | 8080 | Port Spring Boot listens on |
| `DB_URL` | jdbc:postgresql://localhost:5432/multilingual_ai | Postgres connection |
| `DB_USERNAME` / `DB_PASSWORD` | postgres / postgres | DB credentials |
| `AI_SERVICE_URL` | http://localhost:8000 | Base URL of the Python AI service |
| `MAX_UPLOAD_SIZE` | 25MB | Max audio upload size |

## Run

```bash
cd backend
mvn spring-boot:run
```

Swagger UI: http://localhost:8080/swagger-ui.html

## Endpoints

- `POST /api/text/translate` — `{ "text", "sourceLang", "targetLang" }` → translated text
- `POST /api/audio/transcribe` — multipart `file` → transcript
- `POST /api/audio/translate` — multipart `file` + `targetLang` → transcript, translated text, translated audio URL

## Architecture

```
Controller → Service → AiServiceClient (HTTP) → FastAPI AI service
                ↓
           Repository → PostgreSQL (translation history only)
```

Spring Boot never runs AI models directly — every AI operation is a delegated HTTP call via `AiServiceClient`, configured through `AI_SERVICE_URL`.

## Not included by default
- Redis caching (optional per SOP — add once the core pipeline is validated end-to-end)
- Authentication/authorization (explicitly out of scope for this project)
