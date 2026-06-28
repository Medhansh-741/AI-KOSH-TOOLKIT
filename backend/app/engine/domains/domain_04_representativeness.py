from .base import BaseDomainScorer, DomainScoreResult

class RepresentativenessScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 4
    DOMAIN_NAME = "Population Representativeness"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        geo = self.metadata.get("geographic_coverage")
        sites = self.metadata.get("num_sites")
        sex = self.metadata.get("sex_distribution")
        
        if not geo:
            gaps.append("Geographic coverage not declared.")
            return DomainScoreResult(
                domain_number=self.DOMAIN_NUMBER,
                domain_name=self.DOMAIN_NAME,
                score=1,
                rationale="Geographic coverage not declared. Minimum representativeness score.",
                evidence_items=evidence,
                gaps=gaps,
                confidence="Low"
            )
            
        evidence.append(f"Geographic coverage declared: {geo}")
        
        sites_val = int(sites) if sites else 1
        if sites_val > 1:
            evidence.append(f"Multi-site study: {sites_val} sites.")
        else:
            gaps.append("Single site study or sites count not provided.")
            
        if sex:
            evidence.append(f"Sex distribution reported: {sex}")
        else:
            gaps.append("Sex distribution not reported.")
            
        thresholds = self.criteria.get("thresholds", {}) if isinstance(self.criteria, dict) else {}
        multi_site_min = thresholds.get("multi_site_min", 2)
        
        if geo == "national" and sites_val >= multi_site_min and sex:
            score = 4
        elif geo in ["state", "region"] and sites_val >= multi_site_min:
            score = 3
        elif geo in ["district", "taluk", "village"] or sites_val > 1:
            score = 2
        else:
            score = 1
            
        rationale = f"Score {score}: Geographic coverage is {geo} with {sites_val} sites."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
