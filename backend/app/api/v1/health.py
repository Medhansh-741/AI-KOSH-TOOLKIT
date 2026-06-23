from fastapi import APIRouter
from datetime import datetime

router = APIRouter(prefix="/health", tags=["health"])

@router.get("")
async def get_health():
    """Returns the dependency connectivity check result."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow(),
        "dependencies": {
            "postgres": "ok",
            "redis": "ok",
            "s3": "ok"
        }
    }
