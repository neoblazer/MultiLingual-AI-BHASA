package com.multilingualai.backend.entity;

import jakarta.persistence.*;
import java.time.Instant;

/**
 * Minimal persistence: a log of translation requests. Kept simple per
 * SOP — no RAG/vector/knowledge-base tables, just an audit-style record.
 */
@Entity
@Table(name = "translation_records")
public class TranslationRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 10)
    private String sourceLang;

    @Column(nullable = false, length = 10)
    private String targetLang;

    @Column(columnDefinition = "TEXT")
    private String sourceText;

    @Column(columnDefinition = "TEXT")
    private String translatedText;

    @Column(nullable = false)
    private Instant createdAt = Instant.now();

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getSourceLang() { return sourceLang; }
    public void setSourceLang(String sourceLang) { this.sourceLang = sourceLang; }

    public String getTargetLang() { return targetLang; }
    public void setTargetLang(String targetLang) { this.targetLang = targetLang; }

    public String getSourceText() { return sourceText; }
    public void setSourceText(String sourceText) { this.sourceText = sourceText; }

    public String getTranslatedText() { return translatedText; }
    public void setTranslatedText(String translatedText) { this.translatedText = translatedText; }

    public Instant getCreatedAt() { return createdAt; }
    public void setCreatedAt(Instant createdAt) { this.createdAt = createdAt; }
}
