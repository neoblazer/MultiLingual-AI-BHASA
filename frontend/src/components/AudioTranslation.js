import React, { useState } from "react";
import { translateAudio } from "../api/client";
import { LANGUAGES } from "../languages";

export default function AudioTranslation() {
  const [file, setFile] = useState(null);
  const [targetLang, setTargetLang] = useState("en");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleTranslate() {
    setError(null);
    if (!file) {
      setError("Please select an audio file first.");
      return;
    }
    setLoading(true);
    setResult(null);
    try {
      const response = await translateAudio(file, targetLang);
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.message || "Audio translation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  // The backend proxies transcript/translation but the audio URL comes
  // from the AI service directly; assumes AI service runs on port 8000
  // during local development (see README for how this is wired).
  const audioServiceBase = process.env.REACT_APP_AI_SERVICE_URL || "http://localhost:8000";

  return (
    <section style={styles.section}>
      <h2>Audio Translation</h2>

      <div style={styles.row}>
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <label>
          Target language:
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            {LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>{lang.label}</option>
            ))}
          </select>
        </label>
      </div>

      <button onClick={handleTranslate} disabled={loading}>
        {loading ? "Processing..." : "Translate Audio"}
      </button>

      {error && <p style={styles.error}>{error}</p>}

      {result && (
        <div style={styles.resultBox}>
          <p><strong>Transcript ({result.sourceLanguage}):</strong> {result.transcript}</p>
          <p><strong>Translated text:</strong> {result.translatedText}</p>
          {result.translatedAudioUrl && (
            <audio controls src={`${audioServiceBase}${result.translatedAudioUrl}`} />
          )}
        </div>
      )}
    </section>
  );
}

const styles = {
  section: { marginBottom: "2rem", padding: "1rem", border: "1px solid #ddd", borderRadius: "8px" },
  row: { display: "flex", gap: "1rem", alignItems: "center", marginBottom: "1rem" },
  error: { color: "red" },
  resultBox: { marginTop: "1rem", padding: "0.75rem", background: "#f5f5f5", borderRadius: "6px" },
};
