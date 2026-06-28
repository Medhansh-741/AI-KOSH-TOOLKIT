from .base import BaseDomainScorer, DomainScoreResult

class MetadataCompletenessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 2
    DOMAIN_NAME = "Metadata Completeness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        # Count non-empty metadata fields
        key_fields = [
            "dataset_name", "dataset_version", "dataset_type", "study_type",
            "target_population", "geographic_coverage", "collection_start_date",
            "deidentification_method", "standards_used", "license_type"
        ]
        
        filled = 0
        for f in key_fields:
            if self._get_clean_str(f):
                filled += 1
                evidence.append(f"Metadata field '{f}' is populated.")
            else:
                gaps.append(f"Metadata field '{f}' is missing.")
                
        pct = (filled / len(key_fields)) * 100
        thresholds = self.criteria.get("thresholds", {}) if isinstance(self.criteria, dict) else {}
        t1 = float(thresholds.get("tier1", 30.0))
        t2 = float(thresholds.get("tier2", 60.0))
        t3 = float(thresholds.get("tier3", 85.0))
        if pct < t1:
            score = 1
        elif pct < t2:
            score = 2
        elif pct < t3:
            score = 3
        else:
            score = 4
            
        rationale = f"Score {score}: {filled} out of {len(key_fields)} key metadata fields populated ({round(pct, 1)}%)."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
