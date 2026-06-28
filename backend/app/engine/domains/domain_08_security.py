from .base import BaseDomainScorer, DomainScoreResult

class SecurityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 8
    DOMAIN_NAME = "Security & Access Governance"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        control = self._get_clean_str("access_control_method")
        dua = self.metadata.get("dua_required", False)
        
        control_str = (control or "").lower()
        is_public = any(k in control_str for k in ["public", "open"])
        has_rbac = any(k in control_str for k in ["role", "rbac", "vpn", "secure", "identity", "authenticated", "institutional"])
        has_approval = any(k in control_str for k in ["request", "approval", "managed", "permission", "application", "committee"])
        
        if not control:
            gaps.append("No access control method documented.")
            score = 1
        elif is_public:
            evidence.append("Public / open access control documented.")
            score = 2
        elif dua and (has_rbac or has_approval):
            if has_rbac:
                evidence.append("Role-based / authenticated access control with Data Use Agreement (DUA) enforced.")
                score = 4
            else:
                evidence.append("Approval-based access with Data Use Agreement (DUA) requirement documented.")
                score = 3
        elif dua or has_approval or has_rbac:
            evidence.append(f"Controlled access governance documented: {control}")
            score = 3
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
