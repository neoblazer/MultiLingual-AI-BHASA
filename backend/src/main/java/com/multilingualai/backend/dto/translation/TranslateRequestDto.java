package com.multilingualai.backend.dto.translation;

import jakarta.validation.constraints.NotBlank;

public class TranslateRequestDto {

    @NotBlank(message = "text must not be blank")
    private String text;

    @NotBlank(message = "sourceLang must not be blank")
    private String sourceLang;

    @NotBlank(message = "targetLang must not be blank")
    private String targetLang;

    public String getText() { return text; }
    public void setText(String text) { this.text = text; }

    public String getSourceLang() { return sourceLang; }
    public void setSourceLang(String sourceLang) { this.sourceLang = sourceLang; }

    public String getTargetLang() { return targetLang; }
    public void setTargetLang(String targetLang) { this.targetLang = targetLang; }
}
