from sqlalchemy import Column, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from datetime import datetime
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    assessment_id = Column(UUID(as_uuid=True), ForeignKey("assessments.assessment_id", ondelete="CASCADE"), nullable=False, index=True)
    event_type = Column(String, nullable=False)
    event_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    event_detail = Column(JSONB, default=dict, nullable=False)
    component = Column(String, nullable=True)
    severity = Column(Enum("INFO", "WARNING", "ERROR", name="severity_level"), default="INFO", nullable=False)

    # Relationships
    assessment = relationship("Assessment", back_populates="audit_logs")
