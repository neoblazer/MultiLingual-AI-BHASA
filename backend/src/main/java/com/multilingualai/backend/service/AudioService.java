package com.multilingualai.backend.service;

import com.multilingualai.backend.client.ai.AiServiceClient;
import com.multilingualai.backend.dto.audio.AudioTranslateResponseDto;
import com.multilingualai.backend.dto.audio.TranscriptionResponseDto;
import com.multilingualai.backend.exception.InvalidRequestException;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

@Service
public class AudioService {

    private final AiServiceClient aiServiceClient;

    private static final long MAX_FILE_SIZE_BYTES = 25L * 1024 * 1024;

    public AudioService(AiServiceClient aiServiceClient) {
        this.aiServiceClient = aiServiceClient;
    }

    public TranscriptionResponseDto transcribe(MultipartFile audioFile) {
        validateAudioFile(audioFile);
        return aiServiceClient.transcribe(audioFile);
    }

    public AudioTranslateResponseDto translateAudio(MultipartFile audioFile, String targetLang) {
        validateAudioFile(audioFile);
        if (targetLang == null || targetLang.isBlank()) {
            throw new InvalidRequestException("targetLang must be provided.");
        }
        return aiServiceClient.translateAudio(audioFile, targetLang);
    }

    private void validateAudioFile(MultipartFile file) {
        if (file == null || file.isEmpty()) {
            throw new InvalidRequestException("Audio file must not be empty.");
        }
        if (file.getSize() > MAX_FILE_SIZE_BYTES) {
            throw new InvalidRequestException("Audio file exceeds the maximum allowed size (25MB).");
        }
    }
}
