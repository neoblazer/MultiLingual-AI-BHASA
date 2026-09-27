# Frontend — React

## Setup

```bash
cd frontend
npm install
cp .env.example .env
npm start
```

Opens at http://localhost:3000

## What it does
- **Text Translation**: pick source/target language, enter text, get translated text back (calls Spring Boot `/api/text/translate`)
- **Audio Translation**: upload audio, pick target language, get transcript + translated text + a playable translated-audio result (calls Spring Boot `/api/audio/translate`)

## Requirements to actually see results
Both the AI service (port 8000) and Spring Boot backend (port 8080) must be running.
