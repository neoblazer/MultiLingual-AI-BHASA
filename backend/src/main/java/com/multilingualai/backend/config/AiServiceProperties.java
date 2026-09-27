package com.multilingualai.backend.config;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

/**
 * Binds the ai.service.* properties (backed by AI_SERVICE_URL env var,
 * see application.yml) so the AI client never hard-codes a host.
 */
@Configuration
@ConfigurationProperties(prefix = "ai.service")
public class AiServiceProperties {

    private String baseUrl;
    private int connectTimeoutMs = 5000;
    private int readTimeoutMs = 60000;

    public String getBaseUrl() {
        return baseUrl;
    }

    public void setBaseUrl(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public int getConnectTimeoutMs() {
        return connectTimeoutMs;
    }

    public void setConnectTimeoutMs(int connectTimeoutMs) {
        this.connectTimeoutMs = connectTimeoutMs;
    }

    public int getReadTimeoutMs() {
        return readTimeoutMs;
    }

    public void setReadTimeoutMs(int readTimeoutMs) {
        this.readTimeoutMs = readTimeoutMs;
    }
}
