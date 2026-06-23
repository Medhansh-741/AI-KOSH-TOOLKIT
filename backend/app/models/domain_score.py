from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base

class DomainScore(Base):
    __tablename__ = "domain_scores"

    score_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False, index=True)
    domain_number = Column(Integer, nullable=False)
    domain_name = Column(String, nullable=False)
    score = Column(Integer, nullable=True) # None/null if not applicable (e.g. Domain 11)
    max_score = Column(Integer, default=4, nullable=True)
    not_applicable = Column(Boolean, default=False, nullable=False)
    confidence_level = Column(Enum("High", "Medium", "Low", name="confidence_level"), nullable=True)
    rationale = Column(String, nullable=True)
    evidence_items = Column(JSONB, default=list, nullable=False)
    gaps = Column(JSONB, default=list, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="domain_scores")
