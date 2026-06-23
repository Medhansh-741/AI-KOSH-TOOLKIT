from sqlalchemy import Column, String, DateTime, Boolean, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"

    assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataset_id = Column(String, nullable=True, index=True)
    status = Column(Enum("queued", "processing", "complete", "failed", name="assessment_status"), default="queued", nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(String, nullable=True)
    toolkit_version = Column(String, default="1.0.0", nullable=False)
    domain_11_applicable = Column(Boolean, default=False, nullable=False)

    # Relationships
    domain_scores = relationship("DomainScore", back_populates="assessment", cascade="all, delete-orphan")
    result = relationship("AssessmentResult", uselist=False, back_populates="assessment", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="assessment", cascade="all, delete-orphan")
