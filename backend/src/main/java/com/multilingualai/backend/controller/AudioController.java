package com.multilingualai.backend.controller;

import com.multilingualai.backend.dto.audio.AudioTranslateResponseDto;
import com.multilingualai.backend.dto.audio.TranscriptionResponseDto;
import com.multilingualai.backend.service.AudioService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/audio")
public class AudioController {

    private final AudioService audioService;

    public AudioController(AudioService audioService) {
        this.audioService = audioService;
    }

    @PostMapping(value = "/transcribe", consumes = "multipart/form-data")
    public ResponseEntity<TranscriptionResponseDto> transcribe(
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(audioService.transcribe(file));
    }

    @PostMapping(value = "/translate", consumes = "multipart/form-data")
    public ResponseEntity<AudioTranslateResponseDto> translateAudio(
            @RequestParam("file") MultipartFile file,
            @RequestParam("targetLang") String targetLang) {
        return ResponseEntity.ok(audioService.translateAudio(file, targetLang));
    }
}
