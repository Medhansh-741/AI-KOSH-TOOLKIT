from .base import BaseDomainScorer, DomainScoreResult

class ModelLinkageScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 13
    DOMAIN_NAME = "Model Linkage Integrity"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        models = self.metadata.get("linked_model_ids")
        neutral_score = self.criteria.get("neutral_score_when_no_models", 3)
        
        if models is None or (isinstance(models, list) and len(models) == 0):
            evidence.append("No models linked to this dataset (neutral rating applied).")
            score = neutral_score
        else:
            evidence.append(f"Linked model IDs: {models}")
            score = 3
            if isinstance(models, dict) or (isinstance(models, list) and len(models) > 1):
                evidence.append("Multiple models/configurations linked.")
                score = 4
                
        rationale = f"Score {score}: Model linkage is {models or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
