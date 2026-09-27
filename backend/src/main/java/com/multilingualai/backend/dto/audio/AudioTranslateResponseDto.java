package com.multilingualai.backend.dto.audio;

public class AudioTranslateResponseDto {

    private String transcript;
    private String sourceLanguage;
    private String translatedText;
    private String translatedAudioUrl;

    public AudioTranslateResponseDto() {}

    public AudioTranslateResponseDto(String transcript, String sourceLanguage,
                                      String translatedText, String translatedAudioUrl) {
        this.transcript = transcript;
        this.sourceLanguage = sourceLanguage;
        this.translatedText = translatedText;
        this.translatedAudioUrl = translatedAudioUrl;
    }

    public String getTranscript() { return transcript; }
    public void setTranscript(String transcript) { this.transcript = transcript; }

    public String getSourceLanguage() { return sourceLanguage; }
    public void setSourceLanguage(String sourceLanguage) { this.sourceLanguage = sourceLanguage; }

    public String getTranslatedText() { return translatedText; }
    public void setTranslatedText(String translatedText) { this.translatedText = translatedText; }

    public String getTranslatedAudioUrl() { return translatedAudioUrl; }
    public void setTranslatedAudioUrl(String translatedAudioUrl) { this.translatedAudioUrl = translatedAudioUrl; }
}
