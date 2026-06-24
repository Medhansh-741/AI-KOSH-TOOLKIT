from .base import BaseDomainScorer, DomainScoreResult

class StewardshipScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 12
    DOMAIN_NAME = "Stewardship & Governance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        steward = self.metadata.get("named_steward_exists", False)
        dpdp = self.metadata.get("dpdp_compliance_status")
        
        if not steward:
            gaps.append("No named data steward or custodian designated.")
            score = 1
        else:
            evidence.append("Named data steward designated.")
            if dpdp == "compliant":
                evidence.append("DPDP compliant status verified.")
                score = 4
            elif dpdp == "under_review":
                evidence.append("DPDP compliance under review.")
                score = 3
            else:
                gaps.append("DPDP compliance status not verified or non-compliant.")
                score = 2
                
        rationale = f"Score {score}: steward={steward}, DPDP={dpdp}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
