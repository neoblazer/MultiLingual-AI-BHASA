import React from "react";

// A tiny static "waveform" — the one deliberate visual flourish for
// audio mode, standing in for a generic upload icon.
export default function Waveform() {
  const heights = [6, 14, 22, 12, 28, 10, 18, 8, 24, 14, 6];
  return (
    <div className="wave" aria-hidden="true">
      {heights.map((h, i) => (
        <span key={i} style={{ height: `${h}px` }} />
      ))}
    </div>
  );
}
