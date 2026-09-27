package com.multilingualai.backend.dto.translation;

public class TranslateResponseDto {

    private String translatedText;

    public TranslateResponseDto() {}

    public TranslateResponseDto(String translatedText) {
        this.translatedText = translatedText;
    }

    public String getTranslatedText() { return translatedText; }
    public void setTranslatedText(String translatedText) { this.translatedText = translatedText; }
}
