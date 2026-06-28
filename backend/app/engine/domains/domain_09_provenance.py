from .base import BaseDomainScorer, DomainScoreResult

class ProvenanceScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 9
    DOMAIN_NAME = "Provenance & Workflow Transparency"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        pipeline = self.metadata.get("provenance_pipeline_available", False)
        changelog = self.metadata.get("changelog_provided", False)
        ver = self._get_clean_str("version_format")
        start_date = self.metadata.get("collection_start_date")
        end_date = self.metadata.get("collection_end_date")
        temp_gran = self._get_clean_str("temporal_granularity")

        if start_date or end_date:
            evidence.append(f"Temporal data collection span documented ({start_date or 'N/A'} to {end_date or 'N/A'}).")
        if temp_gran:
            evidence.append(f"Temporal resolution documented: {temp_gran}.")

        if not pipeline and not changelog and not ver:
            gaps.append("No provenance metadata provided.")
            score = 1
        elif ver and not pipeline:
            evidence.append(f"Version format defined: {ver}")
            score = 2
        elif pipeline and not changelog:
            evidence.append("Preprocessing data lineage pipeline documented.")
            score = 3
        else:
            evidence.append("Workflow pipeline, version history, and changelog fully available.")
            score = 4
            
        rationale = f"Score {score}: Pipeline={pipeline}, Changelog={changelog}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
