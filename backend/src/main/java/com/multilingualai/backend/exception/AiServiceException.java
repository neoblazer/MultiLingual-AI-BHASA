package com.multilingualai.backend.exception;

public class AiServiceException extends RuntimeException {

    private final int statusCode;

    public AiServiceException(String message, int statusCode) {
        super(message);
        this.statusCode = statusCode;
    }

    public AiServiceException(String message, Throwable cause) {
        super(message, cause);
        this.statusCode = 502; // Bad Gateway - AI service unreachable
    }

    public int getStatusCode() {
        return statusCode;
    }
}
