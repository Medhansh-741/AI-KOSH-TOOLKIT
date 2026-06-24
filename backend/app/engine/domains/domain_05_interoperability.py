from .base import BaseDomainScorer, DomainScoreResult

class InteroperabilityScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 5
    DOMAIN_NAME = "Data Structure & Interoperability"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        data_signals = 3
        meta_signals = 1
        
        comp = self.profile.get("completeness", {})
        overall_pct = comp.get("overall_pct", 100.0)
        standards = self.profile.get("standards_detected", {})
        icd_present = standards.get("icd_codes_present", False)
        fhir_present = standards.get("fhir_structure", False)
        snomed_present = standards.get("snomed_codes_present", False)
        loinc_present = standards.get("loinc_codes_present", False)
        
        evidence.append(f"Overall cell completeness: {overall_pct}%")
        
        if overall_pct < 50.0:
            gaps.append("Extremely low data completeness (<50%).")
            score = 0
        elif overall_pct < 75.0:
            gaps.append("Low data completeness (<75%).")
            score = 1
        elif overall_pct < 90.0:
            gaps.append("Moderate data completeness (<90%).")
            score = 2
        else:
            score = 3
            if icd_present or fhir_present or snomed_present or loinc_present:
                evidence.append("Ontology standards (ICD/SNOMED/LOINC/FHIR) detected in data columns.")
                score = 4
            else:
                gaps.append("No medical coding standards detected in data.")
                
        confidence = self._determine_confidence(data_signals, meta_signals)
        rationale = f"Score {score}: Cell completeness is {overall_pct}%."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence=confidence
        )
