from .base import BaseDomainScorer, DomainScoreResult

class SyntheticDataScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 11
    DOMAIN_NAME = "Synthetic / Simulated Data"

    def score(self) -> DomainScoreResult:
        pct = self.metadata.get("synthetic_data_pct")
        
        if pct is None or float(pct) == 0.0:
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=None,
                rationale="Dataset contains no synthetic or simulated data. Domain excluded from CQI calculation.",
                evidence_items=[],
                gaps=[],
                confidence="Low",
                not_applicable=True
            )
            
        evidence = [f"Synthetic data ratio: {pct}%"]
        gaps = []
        
        utility = self.metadata.get("synthetic_utility_evaluated", False)
        privacy = self.metadata.get("synthetic_privacy_tested", False)
        
        if not utility and not privacy:
            gaps.append("Synthetic utility and privacy not evaluated.")
            score = 1
        elif utility and not privacy:
            evidence.append("Synthetic utility evaluated.")
            gaps.append("Synthetic privacy leakage not tested.")
            score = 2
        elif utility and privacy:
            evidence.append("Synthetic utility and privacy tested.")
            score = 3
            if float(pct) >= 50.0:
                evidence.append("Majority synthetic dataset (>50%).")
                score = 4
        else:
            score = 1
            
        rationale = f"Score {score}: Synthetic pct={pct}%, utility={utility}, privacy={privacy}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
