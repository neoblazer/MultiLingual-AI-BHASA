package com.multilingualai.backend.controller;

import com.multilingualai.backend.dto.translation.TranslateRequestDto;
import com.multilingualai.backend.dto.translation.TranslateResponseDto;
import com.multilingualai.backend.service.TranslationService;
import jakarta.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/text")
public class TranslationController {

    private final TranslationService translationService;

    public TranslationController(TranslationService translationService) {
        this.translationService = translationService;
    }

    @PostMapping("/translate")
    public ResponseEntity<TranslateResponseDto> translate(@Valid @RequestBody TranslateRequestDto request) {
        TranslateResponseDto response = translationService.translate(
                request.getText(), request.getSourceLang(), request.getTargetLang());
        return ResponseEntity.ok(response);
    }
}
