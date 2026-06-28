from .base import BaseDomainScorer, DomainScoreResult

class SustainabilityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 14
    DOMAIN_NAME = "Environmental Sustainability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        fmt = self.profile.get("file", {}).get("format", "csv").lower()
        size = self.profile.get("file", {}).get("size_bytes", 0)
        sust_info = self.metadata.get("sustainability_info_provided", False)
        
        if sust_info:
            evidence.append("Environmental sustainability documentation or energy usage information provided.")
            score = 4
        elif fmt == "parquet":
            evidence.append("Optimized binary column format (Parquet) reduces CPU cycles and storage size.")
            score = 3
        else:
            thresholds = self.criteria.get("thresholds", {}) if isinstance(self.criteria, dict) else {}
            max_bytes = int(thresholds.get("max_file_size_bytes", 10000000))
            if size < max_bytes:
                evidence.append(f"Small file footprint (<{max_bytes} bytes) reduces transmission and analysis carbon costs.")
                score = 3
            else:
                gaps.append("Large raw text file (CSV/XLSX) increases storage and compute footprint.")
                score = 2
            
        rationale = f"Score {score}: Sustainability assessed on size and file format."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Medium"
        )
