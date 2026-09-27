import React, { useState } from "react";
import { translateText } from "../api/client";
import { LANGUAGES } from "../languages";

export default function TextTranslation() {
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("hi");
  const [sourceText, setSourceText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleTranslate() {
    setError(null);
    if (!sourceText.trim()) {
      setError("Please enter some text to translate.");
      return;
    }
    setLoading(true);
    setTranslatedText("");
    try {
      const response = await translateText(sourceText, sourceLang, targetLang);
      setTranslatedText(response.data.translatedText);
    } catch (err) {
      setError(err.response?.data?.message || "Translation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section style={styles.section}>
      <h2>Text Translation</h2>

      <div style={styles.row}>
        <label>
          Source language:
          <select value={sourceLang} onChange={(e) => setSourceLang(e.target.value)}>
            {LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>{lang.label}</option>
            ))}
          </select>
        </label>

        <label>
          Target language:
          <select value={targetLang} onChange={(e) => setTargetLang(e.target.value)}>
            {LANGUAGES.map((lang) => (
              <option key={lang.code} value={lang.code}>{lang.label}</option>
            ))}
          </select>
        </label>
      </div>

      <textarea
        style={styles.textarea}
        placeholder="Enter text to translate..."
        value={sourceText}
        onChange={(e) => setSourceText(e.target.value)}
        rows={4}
      />

      <button onClick={handleTranslate} disabled={loading}>
        {loading ? "Translating..." : "Translate"}
      </button>

      {error && <p style={styles.error}>{error}</p>}

      {translatedText && (
        <div style={styles.resultBox}>
          <strong>Translated text:</strong>
          <p>{translatedText}</p>
        </div>
      )}
    </section>
  );
}

const styles = {
  section: { marginBottom: "2rem", padding: "1rem", border: "1px solid #ddd", borderRadius: "8px" },
  row: { display: "flex", gap: "1rem", marginBottom: "1rem" },
  textarea: { width: "100%", marginBottom: "0.5rem" },
  error: { color: "red" },
  resultBox: { marginTop: "1rem", padding: "0.75rem", background: "#f5f5f5", borderRadius: "6px" },
};
