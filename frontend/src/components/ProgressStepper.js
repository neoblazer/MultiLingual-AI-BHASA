import React from "react";

const STEPS = ["Transcribing", "Translating", "Generating audio"];

export default function ProgressStepper({ activeStep }) {
  return (
    <div className="stepper">
      {STEPS.map((label, i) => (
        <div key={label} className={`stepper__step ${i <= activeStep ? "stepper__step--active" : ""}`}>
          <span className="stepper__dot" />
          <span className="stepper__label">{label}</span>
          {i < STEPS.length - 1 && <span className="stepper__line" />}
        </div>
      ))}
    </div>
  );
}
