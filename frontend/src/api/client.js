import axios from "axios";

// Configurable via .env: REACT_APP_BACKEND_URL — never hard-code the
// backend host, same principle as the AI_SERVICE_URL on the backend.
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || "http://localhost:8080";

export const api = axios.create({
  baseURL: BACKEND_URL,
});

export function translateText(text, sourceLang, targetLang) {
  return api.post("/api/text/translate", {
    text,
    sourceLang,
    targetLang,
  });
}

export function translateAudio(file, targetLang) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("targetLang", targetLang);

  return api.post("/api/audio/translate", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}
