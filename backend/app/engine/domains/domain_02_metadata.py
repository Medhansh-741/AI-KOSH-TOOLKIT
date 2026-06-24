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
            if self.metadata.get(f):
                filled += 1
                evidence.append(f"Metadata field '{f}' is populated.")
            else:
                gaps.append(f"Metadata field '{f}' is missing.")
                
        pct = (filled / len(key_fields)) * 100
        if pct < 30:
            score = 1
        elif pct < 60:
            score = 2
        elif pct < 85:
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
