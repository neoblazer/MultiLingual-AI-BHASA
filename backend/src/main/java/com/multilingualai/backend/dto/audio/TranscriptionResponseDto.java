package com.multilingualai.backend.dto.audio;

public class TranscriptionResponseDto {

    private String transcript;
    private String detectedLanguage;
    private Double durationSeconds;

    public TranscriptionResponseDto() {}

    public TranscriptionResponseDto(String transcript, String detectedLanguage, Double durationSeconds) {
        this.transcript = transcript;
        this.detectedLanguage = detectedLanguage;
        this.durationSeconds = durationSeconds;
    }

    public String getTranscript() { return transcript; }
    public void setTranscript(String transcript) { this.transcript = transcript; }

    public String getDetectedLanguage() { return detectedLanguage; }
    public void setDetectedLanguage(String detectedLanguage) { this.detectedLanguage = detectedLanguage; }

    public Double getDurationSeconds() { return durationSeconds; }
    public void setDurationSeconds(Double durationSeconds) { this.durationSeconds = durationSeconds; }
}
