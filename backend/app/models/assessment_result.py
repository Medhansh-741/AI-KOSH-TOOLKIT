from sqlalchemy import Column, Numeric, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database import Base

class AssessmentResult(Base):
    __tablename__ = "assessment_results"

    result_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False, index=True)
    cqi = Column(Numeric(precision=4, scale=1), nullable=False)
    cqi_band = Column(String, nullable=False)
    prs = Column(Integer, nullable=False)
    prs_band = Column(String, nullable=False)
    release_classification = Column(Enum("Open", "Controlled", "Restricted", name="release_class"), nullable=False)
    classification_justification = Column(String, nullable=False)
    
    # Store S3 report URLs
    report_urls = Column(JSONB, default=dict, nullable=False) # e.g. {"json": "url", "html": "url", "pdf": "url"}
    
    # Store dataset profiling summary JSON directly
    profile_summary = Column(JSONB, default=dict, nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="result")
