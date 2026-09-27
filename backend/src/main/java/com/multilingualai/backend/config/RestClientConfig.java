package com.multilingualai.backend.config;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.PropertyNamingStrategies;
import org.springframework.boot.web.client.RestTemplateBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.web.client.RestTemplate;

import java.time.Duration;

/**
 * Provides a RestTemplate used by the AI client to talk to the Python
 * FastAPI service over HTTP.
 *
 * FastAPI/Pydantic use snake_case JSON field names (e.g. "source_lang",
 * "detected_language"), while Java/Jackson conventionally use camelCase
 * ("sourceLang", "detectedLanguage"). Rather than manually renaming
 * fields at every call site, this RestTemplate uses a dedicated
 * ObjectMapper with SNAKE_CASE naming, so DTOs can just use normal
 * Java camelCase field names and Jackson handles the translation
 * automatically in both directions for AI-service calls only. The
 * frontend-facing DTOs (via @RequestBody/@ResponseBody) are unaffected
 * and keep using plain camelCase JSON, since Spring MVC uses its own
 * default ObjectMapper for those.
 */
@Configuration
public class RestClientConfig {

    @Bean
    public RestTemplate aiServiceRestTemplate(RestTemplateBuilder builder,
                                               AiServiceProperties properties) {
        ObjectMapper snakeCaseMapper = new ObjectMapper()
                .setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);

        RestTemplate restTemplate = builder
                .setConnectTimeout(Duration.ofMillis(properties.getConnectTimeoutMs()))
                .setReadTimeout(Duration.ofMillis(properties.getReadTimeoutMs()))
                .build();

        restTemplate.getMessageConverters().add(0,
                new MappingJackson2HttpMessageConverter(snakeCaseMapper));

        return restTemplate;
    }
}
