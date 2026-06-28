from .base import BaseDomainScorer, DomainScoreResult

class CurationScorer(BaseDomainScorer):
    DOMAIN_NUMBER = 15
    DOMAIN_NAME = "Continuous Curation & Feedback"

    def score(self) -> DomainScoreResult:
        evidence = []
        gaps = []
        
        repo = self._get_clean_str("github_repo_url")
        changelog = self.metadata.get("changelog_provided", False)
        
        if not repo and not changelog:
            gaps.append("No active repository or version changelog provided.")
            score = 1
        elif repo and not changelog:
            evidence.append(f"Active code/data repository: {repo}")
            score = 2
        elif changelog and not repo:
            evidence.append("Changelog/updates documentation provided.")
            score = 3
        else:
            evidence.append("Active repository and detailed changelog provided.")
            score = 4
            
        rationale = f"Score {score}: Repo={bool(repo)}, Changelog={changelog}."
        
        return DomainScoreResult(
            domain_number=self.DOMAIN_NUMBER,
            domain_name=self.DOMAIN_NAME,
            score=score,
            rationale=rationale,
            evidence_items=evidence,
            gaps=gaps,
            confidence="Low"
        )
