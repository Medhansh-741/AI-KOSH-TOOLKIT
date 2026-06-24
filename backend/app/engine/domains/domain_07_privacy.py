from .base import BaseDomainScorer, DomainScoreResult

class PrivacyScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 7
    DOMAIN_NAME = "Privacy & Identifiability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        data_signals = 2
        meta_signals = 3
        
        pii = self.profile.get("pii_scan", {})
        direct_ids = pii.get("direct_identifiers_detected", False)
        
        if direct_ids:
            gaps.append("Direct identifiers (name, phone, GPS or ID) detected in column headers.")
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=0,
                rationale="Direct PII identifiers found in dataset.",
                evidence_items=evidence,
                gaps=gaps,
                confidence="High"
            )
            
        evidence.append("No direct identifiers found in dataset.")
        
        deident = self.metadata.get("deidentification_method")
        dp_applied = self.metadata.get("differential_privacy_applied", False)
        k_val = self.metadata.get("k_anonymity_value")
        
        if not deident:
            gaps.append("No de-identification method declared.")
            score = 1
        elif dp_applied:
            evidence.append("Differential Privacy applied.")
            score = 4
        elif k_val and int(k_val) >= 10:
            evidence.append(f"k-anonymity verified with k={k_val}.")
            score = 4
        elif k_val and int(k_val) >= 5:
            evidence.append(f"k-anonymity verified with k={k_val}.")
            score = 3
        else:
            evidence.append(f"De-identification applied: {deident}")
            score = 2
            
        confidence = self._determine_confidence(data_signals, meta_signals)
        rationale = f"Score {score}: Direct identifiers absent. De-identification is {deident or 'absent'}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence=confidence
        )
