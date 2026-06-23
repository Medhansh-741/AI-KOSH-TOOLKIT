from sqlalchemy.orm import Session
from app.models.audit_log import AuditLog
from typing import Dict, Any, Literal
from uuid import UUID

class AuditService:
    @staticmethod
    def log_event(
        db: Session,
        assessment_id: UUID,
        event_type: str,
        event_detail: Dict[str, Any],
        component: str,
        severity: Literal["INFO", "WARNING", "ERROR"] = "INFO"
    ) -> AuditLog:
        """Inserts a structured audit log event into the database."""
        log = AuditLog(
            assessment_id=assessment_id,
            event_type=event_type,
            event_detail=event_detail,
            component=component,
            severity=severity
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

audit_service = AuditService()
