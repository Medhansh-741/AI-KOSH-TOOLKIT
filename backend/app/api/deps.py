from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_db
from app.config import settings

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)

from typing import Optional
from fastapi import Query

async def verify_api_key(
    api_key: Optional[str] = Security(api_key_header),
    api_key_query: Optional[str] = Query(None, alias="api_key")
) -> str:
    """Verifies that the provided API key matches the system secret."""
    key = api_key or api_key_query
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key in Authorization Header or query parameter"
        )
    
    # Strip 'Bearer ' if present
    token = key.replace("Bearer ", "") if key.startswith("Bearer ") else key
    
    if token != settings.API_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return token
