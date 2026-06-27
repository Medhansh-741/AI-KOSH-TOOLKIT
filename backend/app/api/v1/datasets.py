from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.database import get_async_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.assessment import Assessment
from app.schemas.assessment import PaginatedAssessmentListResponse, AssessmentListItem

router = APIRouter(prefix="/datasets", tags=["datasets"])

@router.get(
    "/{dataset_id}/assessments",
    response_model=PaginatedAssessmentListResponse,
    status_code=status.HTTP_200_OK
)
async def list_dataset_assessments(
    dataset_id: str,
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    status_filter: Optional[str] = Query(None, alias="status"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """Retrieves assessment history for a specific AIKosh dataset ID."""
    query = select(Assessment).where(Assessment.dataset_id == dataset_id)
    if status_filter:
        query = query.where(Assessment.status == status_filter)
        
    # Count query
    count_query = select(func.count()).select_from(query.subquery())
    total_res = await db.execute(count_query)
    total = total_res.scalar_one()
    
    # Paginated items query
    stmt = query.order_by(desc(Assessment.submission_timestamp)).offset(offset).limit(limit)
    res = await db.execute(stmt)
    assessments = res.scalars().all()
    
    items = []
    for a in assessments:
        item = AssessmentListItem(
            assessment_id=a.assessment_id,
            dataset_id=a.dataset_id,
            status=a.status,
            submission_timestamp=a.submission_timestamp,
            completion_timestamp=a.completion_timestamp,
            cqi=a.result.cqi if a.result else None,
            cqi_band=a.result.cqi_band if a.result else None,
            prs=a.result.prs if a.result else None,
            prs_band=a.result.prs_band if a.result else None,
            release_classification=a.result.release_classification if a.result else None
        )
        items.append(item)
        
    return PaginatedAssessmentListResponse(
        total=total,
        limit=limit,
        offset=offset,
        items=items
    )
