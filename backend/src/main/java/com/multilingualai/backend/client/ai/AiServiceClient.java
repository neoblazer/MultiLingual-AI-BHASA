package com.multilingualai.backend.client.ai;

import com.multilingualai.backend.config.AiServiceProperties;
import com.multilingualai.backend.dto.audio.AudioTranslateResponseDto;
import com.multilingualai.backend.dto.audio.TranscriptionResponseDto;
import com.multilingualai.backend.dto.translation.TranslateRequestDto;
import com.multilingualai.backend.dto.translation.TranslateResponseDto;
import com.multilingualai.backend.exception.AiServiceException;
import com.multilingualai.backend.exception.InvalidRequestException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.HttpClientErrorException;
import org.springframework.web.client.HttpServerErrorException;
import org.springframework.web.client.ResourceAccessException;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;

/**
 * Sole point of communication between Spring Boot and the Python AI
 * service. Spring Boot never runs any model itself — every AI
 * operation is delegated here as a plain HTTP call.
 *
 * Base URL is fully configurable (AI_SERVICE_URL env var) — never
 * hard-coded, per the SOP.
 */
@Component
public class AiServiceClient {

    private static final Logger logger = LoggerFactory.getLogger(AiServiceClient.class);

    private final RestTemplate restTemplate;
    private final AiServiceProperties properties;

    public AiServiceClient(RestTemplate aiServiceRestTemplate, AiServiceProperties properties) {
        this.restTemplate = aiServiceRestTemplate;
        this.properties = properties;
    }

    public TranscriptionResponseDto transcribe(MultipartFile audioFile) {
        String url = properties.getBaseUrl() + "/api/transcribe";

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", toResource(audioFile));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(body, headers);

        try {
            ResponseEntity<TranscriptionResponseDto> response = restTemplate.postForEntity(
                    url, request, TranscriptionResponseDto.class);
            return response.getBody();
        } catch (HttpClientErrorException e) {
            throw mapClientError(e);
        } catch (HttpServerErrorException e) {
            throw new AiServiceException("AI service failed to process the audio.", e.getStatusCode().value());
        } catch (ResourceAccessException e) {
            throw new AiServiceException("AI service is unavailable or timed out.", e);
        }
    }

    public TranslateResponseDto translate(String text, String sourceLang, String targetLang) {
        String url = properties.getBaseUrl() + "/api/translate";

        TranslateRequestDto payload = new TranslateRequestDto();
        payload.setText(text);
        payload.setSourceLang(sourceLang);
        payload.setTargetLang(targetLang);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<TranslateRequestDto> request = new HttpEntity<>(payload, headers);

        try {
            ResponseEntity<TranslateResponseDto> response = restTemplate.postForEntity(
                    url, request, TranslateResponseDto.class);
            return response.getBody();
        } catch (HttpClientErrorException e) {
            throw mapClientError(e);
        } catch (HttpServerErrorException e) {
            throw new AiServiceException("AI service failed to translate the text.", e.getStatusCode().value());
        } catch (ResourceAccessException e) {
            throw new AiServiceException("AI service is unavailable or timed out.", e);
        }
    }

    public AudioTranslateResponseDto translateAudio(MultipartFile audioFile, String targetLang) {
        String url = properties.getBaseUrl() + "/api/audio/translate";

        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", toResource(audioFile));
        body.add("target_lang", targetLang);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);
        HttpEntity<MultiValueMap<String, Object>> request = new HttpEntity<>(body, headers);

        try {
            ResponseEntity<AudioTranslateResponseDto> response = restTemplate.postForEntity(
                    url, request, AudioTranslateResponseDto.class);
            return response.getBody();
        } catch (HttpClientErrorException e) {
            throw mapClientError(e);
        } catch (HttpServerErrorException e) {
            throw new AiServiceException("AI service failed to process the audio pipeline.", e.getStatusCode().value());
        } catch (ResourceAccessException e) {
            throw new AiServiceException("AI service is unavailable or timed out.", e);
        }
    }

    private RuntimeException mapClientError(HttpClientErrorException e) {
        if (e.getStatusCode() == HttpStatus.BAD_REQUEST || e.getStatusCode() == HttpStatus.UNPROCESSABLE_ENTITY) {
            return new InvalidRequestException(e.getResponseBodyAsString());
        }
        return new AiServiceException(e.getResponseBodyAsString(), e.getStatusCode().value());
    }

    private ByteArrayResource toResource(MultipartFile file) {
        try {
            return new ByteArrayResource(file.getBytes()) {
                @Override
                public String getFilename() {
                    return file.getOriginalFilename();
                }
            };
        } catch (IOException e) {
            throw new InvalidRequestException("Could not read uploaded file: " + e.getMessage());
        }
    }
}
