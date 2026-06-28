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
        elif size < 10000000: # < 10MB
            evidence.append("Small file footprint reduces transmission and analysis carbon costs.")
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
