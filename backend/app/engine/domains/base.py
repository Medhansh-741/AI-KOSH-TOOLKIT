from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class DomainScoreResult(BaseModel):
    domain_number: int
    domain_name: str
    score: Optional[int] = None
    max_score: Optional[int] = 4
    rationale: str
    evidence_items: List[str]
    gaps: List[str]
    confidence: Optional[str] = "Low"
    not_applicable: bool = False

class BaseDomainScorer(ABC):
    def __init__(self, profile: Dict[str, Any], metadata: Dict[str, Any], criteria: Dict[str, Any]):
        self.profile = profile
        self.metadata = metadata
        self.criteria = criteria

    @abstractmethod
    def score(self) -> DomainScoreResult:
        """Computes the 0-4 score. Must be overridden by subclasses."""
        pass

    def _determine_confidence(self, data_signals: int, meta_signals: int) -> str:
        """High if majority from DATA, Low if entirely from META."""
        if data_signals >= meta_signals:
            return "High"
        if meta_signals > 0 and data_signals > 0:
            return "Medium"
        return "Low"

