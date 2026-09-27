package com.multilingualai.backend.repository;

import com.multilingualai.backend.entity.TranslationRecord;
import org.springframework.data.jpa.repository.JpaRepository;

public interface TranslationRecordRepository extends JpaRepository<TranslationRecord, Long> {
}
