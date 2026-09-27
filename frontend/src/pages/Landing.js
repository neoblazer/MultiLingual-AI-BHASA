import React from "react";
import "./Landing.css";
import TranslationWorkspace from "../components/TranslationWorkspace";
import FeatureShowcase from "../components/FeatureShowcase";

export default function Landing() {
  return (
    <>
      <section className="hero">
        <h1 className="hero__title">Bhāṣā</h1>
        <p className="hero__sub">
          Type a sentence or upload a voice clip, and get it back in another
          language — as text, or spoken aloud.
        </p>
        <div className="hero__pills">
          <span className="hero__pill">Speech recognition</span>
          <span className="hero__pill">Neural translation</span>
          <span className="hero__pill">Speech generation</span>
        </div>
      </section>

      <TranslationWorkspace />

      <FeatureShowcase />
    </>
  );
}
