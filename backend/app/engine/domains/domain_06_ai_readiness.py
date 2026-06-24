from .base import BaseDomainScorer, DomainScoreResult

class AIReadinessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 6
    DOMAIN_NAME = "AI / Analytics Readiness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        fmt = self.profile.get("file", {}).get("format", "csv").lower()
        has_dict = self.metadata.get("data_dictionary_uploaded", False)
        has_pipeline = self.metadata.get("provenance_pipeline_available", False)
        
        evidence.append(f"File format is {fmt}.")
        
        if fmt not in ["csv", "parquet", "json", "xlsx"]:
            gaps.append("Proprietary or unoptimized file format.")
            score = 1
        elif not has_dict:
            gaps.append("Data dictionary not uploaded.")
            score = 2
        elif not has_pipeline:
            gaps.append("Data preprocessing pipeline script not linked.")
            score = 3
        else:
            evidence.append("Data dictionary and pipeline script present.")
            score = 4
            
        rationale = f"Score {score}: Format is {fmt} with dictionary={has_dict}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Medium"
        )
