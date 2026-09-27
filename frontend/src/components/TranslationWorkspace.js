import React, { useState, useRef, useEffect } from "react";
import "./TranslationWorkspace.css";
import Waveform from "./Waveform";
import ProgressStepper from "./ProgressStepper";
import { translateText, translateAudio } from "../api/client";
import { LANGUAGES } from "../languages";

const AI_SERVICE_URL = process.env.REACT_APP_AI_SERVICE_URL || "http://localhost:8000";
const HISTORY_KEY = "bhasa_history";
const MAX_HISTORY = 8;

function loadHistory() {
  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
  } catch {
    return [];
  }
}

export default function TranslationWorkspace() {
  const [mode, setMode] = useState("text"); // "text" | "audio"
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("hi");
  const [swapped, setSwapped] = useState(false);

  const [sourceText, setSourceText] = useState("");
  const [translatedText, setTranslatedText] = useState("");

  const [audioFile, setAudioFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [transcript, setTranscript] = useState(null);
  const [detectedLang, setDetectedLang] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const [loading, setLoading] = useState(false);
  const [step, setStep] = useState(0);
  const [error, setError] = useState(null);
  const [copied, setCopied] = useState(false);
  const [history, setHistory] = useState(loadHistory);
  const fileInputRef = useRef(null);
  const stepTimerRef = useRef(null);

  function handleSwap() {
    setSwapped((s) => !s);
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setTranslatedText("");
    setSourceText(translatedText);
  }

  function resetResults() {
    setTranslatedText("");
    setTranscript(null);
    setDetectedLang(null);
    setAudioUrl(null);
    setError(null);
    setCopied(false);
  }

  function pushHistory(entry) {
    setHistory((prev) => {
      const next = [entry, ...prev].slice(0, MAX_HISTORY);
      localStorage.setItem(HISTORY_KEY, JSON.stringify(next));
      return next;
    });
  }

  function startFakeProgress() {
    setStep(0);
    let current = 0;
    stepTimerRef.current = setInterval(() => {
      current += 1;
      if (current <= 2) setStep(current);
    }, 1400);
  }

  function stopFakeProgress() {
    if (stepTimerRef.current) clearInterval(stepTimerRef.current);
    setStep(0);
  }

  useEffect(() => () => stopFakeProgress(), []);

  async function handleTranslateText() {
    if (!sourceText.trim()) {
      setError("Enter some text first.");
      return;
    }
    resetResults();
    setLoading(true);
    try {
      const response = await translateText(sourceText, sourceLang, targetLang);
      setTranslatedText(response.data.translatedText);
      pushHistory({
        mode: "text",
        sourceLang,
        targetLang,
        sourceText,
        translatedText: response.data.translatedText,
        timestamp: Date.now(),
      });
    } catch (err) {
      setError(err.response?.data?.message || "Translation failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  async function handleTranslateAudio() {
    if (!audioFile) {
      setError("Choose or drop an audio file first.");
      return;
    }
    resetResults();
    setLoading(true);
    startFakeProgress();
    try {
      const response = await translateAudio(audioFile, targetLang);
      setTranscript(response.data.transcript);
      setDetectedLang(response.data.sourceLanguage);
      setTranslatedText(response.data.translatedText);
      if (response.data.translatedAudioUrl) {
        setAudioUrl(`${AI_SERVICE_URL}${response.data.translatedAudioUrl}`);
      }
      pushHistory({
        mode: "audio",
        targetLang,
        fileName: audioFile.name,
        transcript: response.data.transcript,
        translatedText: response.data.translatedText,
        timestamp: Date.now(),
      });
    } catch (err) {
      setError(err.response?.data?.message || "Audio translation failed. Please try again.");
    } finally {
      setLoading(false);
      stopFakeProgress();
    }
  }

  function handleFileChange(file) {
    if (file) {
      setAudioFile(file);
      resetResults();
    }
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    handleFileChange(file);
  }

  function handleCopy() {
    if (!translatedText) return;
    navigator.clipboard.writeText(translatedText).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    });
  }

  function loadFromHistory(entry) {
    if (entry.mode === "text") {
      setMode("text");
      setSourceLang(entry.sourceLang);
      setTargetLang(entry.targetLang);
      setSourceText(entry.sourceText);
      setTranslatedText(entry.translatedText);
      setError(null);
    }
  }

  const targetLabel = LANGUAGES.find((l) => l.code === targetLang)?.label;
  const sourceLabel = LANGUAGES.find((l) => l.code === sourceLang)?.label;

  return (
    <div className="workspace-wrap">
      <div className="workspace">
        <div className="tabs">
          <button
            className={`tabs__btn ${mode === "text" ? "tabs__btn--active" : ""}`}
            onClick={() => { setMode("text"); resetResults(); }}
          >
            Text
          </button>
          <button
            className={`tabs__btn ${mode === "audio" ? "tabs__btn--active" : ""}`}
            onClick={() => { setMode("audio"); resetResults(); }}
          >
            Audio
          </button>
        </div>

        <p className="workspace__hint">
          {mode === "text"
            ? "Type text in the source language and get it translated into the target language."
            : "Upload a voice recording to get a transcript, translated text, and translated audio."}
        </p>

        <div className="langbar">
          <select
            className="langbar__select"
            value={sourceLang}
            onChange={(e) => setSourceLang(e.target.value)}
            aria-label="Source language"
          >
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>{l.label}</option>
            ))}
          </select>

          {mode === "text" ? (
            <button
              className={`langbar__swap ${swapped ? "langbar__swap--spun" : ""}`}
              onClick={handleSwap}
              aria-label="Swap languages"
              title="Swap languages"
            >
              ⇄
            </button>
          ) : (
            <span aria-hidden="true" style={{ width: 36 }} />
          )}

          <select
            className="langbar__select langbar__select--target"
            value={targetLang}
            onChange={(e) => setTargetLang(e.target.value)}
            aria-label="Target language"
          >
            {LANGUAGES.map((l) => (
              <option key={l.code} value={l.code}>{l.label}</option>
            ))}
          </select>
        </div>

        {mode === "text" ? (
          <div className="split">
            <div className="split__pane split__pane--source">
              <p className="split__label">{sourceLabel}</p>
              <textarea
                className="split__textarea"
                placeholder="Type something to translate…"
                value={sourceText}
                onChange={(e) => setSourceText(e.target.value)}
              />
              <span className="split__count">{sourceText.length} characters</span>
            </div>
            <div className="split__pane split__pane--target">
              <p className="split__label">{targetLabel}</p>
              {translatedText ? (
                <>
                  <p className="split__output">{translatedText}</p>
                  <button className="split__action" onClick={handleCopy}>
                    {copied ? "Copied ✓" : "Copy"}
                  </button>
                </>
              ) : (
                <p className="split__placeholder">Translation appears here</p>
              )}
            </div>
          </div>
        ) : (
          <div className="split">
            <div className="split__pane split__pane--source">
              <p className="split__label">Source audio</p>
              <div
                className={`dropzone ${dragActive ? "dropzone--active" : ""}`}
                onClick={() => fileInputRef.current?.click()}
                onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
                onDragLeave={() => setDragActive(false)}
                onDrop={handleDrop}
              >
                <Waveform />
                {audioFile ? (
                  <span className="dropzone__filename">{audioFile.name}</span>
                ) : (
                  <>
                    <span className="dropzone__filename">Drop an audio file</span>
                    <span className="dropzone__hint">or click to browse — wav, mp3, m4a</span>
                  </>
                )}
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="audio/*"
                  onChange={(e) => handleFileChange(e.target.files?.[0])}
                />
              </div>
            </div>
            <div className="split__pane split__pane--target">
              <p className="split__label">{targetLabel}</p>
              {loading ? (
                <ProgressStepper activeStep={step} />
              ) : translatedText ? (
                <>
                  <p className="split__output">{translatedText}</p>
                  {audioUrl && (
                    <div className="split__audio-row">
                      <audio className="split__audio" controls src={audioUrl} />
                      <a className="split__action" href={audioUrl} download="translated_audio.wav">
                        Download
                      </a>
                    </div>
                  )}
                </>
              ) : (
                <p className="split__placeholder">Transcript and translation appear here</p>
              )}
            </div>
          </div>
        )}

        {mode === "audio" && transcript && (
          <p className="transcript-note">
            <strong>Transcript{detectedLang ? ` (${detectedLang})` : ""}:</strong> {transcript}
          </p>
        )}

        <div className="actionbar">
          {error ? <p className="actionbar__error">{error}</p> : <span className="actionbar__spacer" />}
          <button
            className="btn-primary"
            onClick={mode === "text" ? handleTranslateText : handleTranslateAudio}
            disabled={loading}
          >
            {loading ? "Working…" : "Translate"}
          </button>
        </div>
      </div>

      {history.length > 0 && (
        <div className="history">
          <p className="history__title">Recent</p>
          <div className="history__list">
            {history.map((entry) => (
              <button
                key={entry.timestamp}
                className="history__item"
                onClick={() => loadFromHistory(entry)}
                disabled={entry.mode === "audio"}
                title={entry.mode === "audio" ? "Audio history is view-only" : "Load back into workspace"}
              >
                <span className="history__badge">{entry.mode === "text" ? "Aa" : "🎙"}</span>
                <span className="history__snippet">
                  {entry.mode === "text" ? entry.sourceText : entry.fileName}
                </span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
