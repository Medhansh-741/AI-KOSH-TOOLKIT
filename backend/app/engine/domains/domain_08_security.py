from .base import BaseDomainScorer, DomainScoreResult

class SecurityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 8
    DOMAIN_NAME = "Security & Access Governance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        control = self.metadata.get("access_control_method")
        dua = self.metadata.get("dua_required", False)
        
        if not control:
            gaps.append("No access control method documented.")
            score = 1
        elif "public" in control.lower() or "open" in control.lower():
            evidence.append("Public access control.")
            score = 2
        elif dua and ("request" in control.lower() or "approval" in control.lower()):
            evidence.append("Approval-based access with Data Use Agreement (DUA) requirement.")
            score = 3
            if "role" in control.lower() or "secure" in control.lower():
                evidence.append("Role-based access controls (RBAC) enforced.")
                score = 4
        else:
            evidence.append(f"Access control documented: {control}")
            score = 2
            
        rationale = f"Score {score}: Access control is {control or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
