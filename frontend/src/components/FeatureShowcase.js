import React, { useState } from "react";
import "./FeatureShowcase.css";

const FEATURES = [
  {
    icon: "🎬",
    title: "Video Translation",
    desc: "Upload a video and get it back with the original audio track replaced by a translated one, synced to the visuals.",
    detail: "Video Translation will extract the audio track, run it through the same speech-to-text, translation, and speech-generation pipeline, then remux the result back into the original video.",
  },
  {
    icon: "💬",
    title: "Subtitle Generation",
    desc: "Automatically generate timed subtitles in the target language from any audio or video source.",
    detail: "Subtitle Generation will produce time-aligned captions in the target language directly from the transcript and translation stages, exportable as standard .srt files.",
  },
  {
    icon: "⚡",
    title: "Real-Time Speech Translation",
    desc: "Speak into your microphone and hear the translation back with minimal delay — no file upload needed.",
    detail: "Real-Time Speech Translation will stream microphone audio through the pipeline in short chunks, aiming for near-live translated speech output during a conversation.",
  },
  {
    icon: "🗣️",
    title: "Speaker Voice Preservation",
    desc: "Keep the original speaker's tone and voice characteristics in the translated audio, instead of a generic voice.",
    detail: "Speaker Voice Preservation will condition speech generation on the original speaker's vocal characteristics, so translated audio sounds like the same person, not a generic narrator.",
  },
];

export default function FeatureShowcase() {
  const [active, setActive] = useState(null);

  return (
    <section className="showcase">
      <div className="showcase__heading">
        <h2 className="showcase__title">What's next</h2>
        <p className="showcase__sub">Planned capabilities building on the same pipeline.</p>
      </div>

      <div className="showcase__grid">
        {FEATURES.map((f) => (
          <button
            key={f.title}
            className="feature-card"
            onClick={() => setActive(f)}
            aria-haspopup="dialog"
          >
            <span className="feature-card__badge">Coming soon</span>
            <span className="feature-card__icon" aria-hidden="true">{f.icon}</span>
            <p className="feature-card__title">{f.title}</p>
            <p className="feature-card__desc">{f.desc}</p>
          </button>
        ))}
      </div>

      {active && (
        <div className="modal-backdrop" role="dialog" aria-modal="true" onClick={() => setActive(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h3 className="modal__title">{active.icon} {active.title}</h3>
            <p className="modal__body">{active.detail}</p>
            <button className="modal__close" onClick={() => setActive(null)}>Got it</button>
          </div>
        </div>
      )}
    </section>
  );
}
