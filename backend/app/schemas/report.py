from pydantic import BaseModel
from typing import Dict, Any
from uuid import UUID

class ReportDownloadResponse(BaseModel):
    assessment_id: UUID
    format: str
    download_url: str
