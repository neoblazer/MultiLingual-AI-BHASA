package com.multilingualai.backend.service;

import com.multilingualai.backend.client.ai.AiServiceClient;
import com.multilingualai.backend.dto.translation.TranslateResponseDto;
import com.multilingualai.backend.entity.TranslationRecord;
import com.multilingualai.backend.repository.TranslationRecordRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

@Service
public class TranslationService {

    private static final Logger logger = LoggerFactory.getLogger(TranslationService.class);

    private final AiServiceClient aiServiceClient;
    private final TranslationRecordRepository repository;

    public TranslationService(AiServiceClient aiServiceClient, TranslationRecordRepository repository) {
        this.aiServiceClient = aiServiceClient;
        this.repository = repository;
    }

    public TranslateResponseDto translate(String text, String sourceLang, String targetLang) {
        TranslateResponseDto result = aiServiceClient.translate(text, sourceLang, targetLang);

        try {
            TranslationRecord record = new TranslationRecord();
            record.setSourceLang(sourceLang);
            record.setTargetLang(targetLang);
            record.setSourceText(text);
            record.setTranslatedText(result.getTranslatedText());
            repository.save(record);
        } catch (Exception e) {
            // Persistence is best-effort logging, not critical path —
            // don't fail the user-facing request if the DB write fails.
            logger.warn("Failed to persist translation record: {}", e.getMessage());
        }

        return result;
    }
}
