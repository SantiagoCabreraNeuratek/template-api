"""
Health check endpoints.
"""
from fastapi import APIRouter, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint",
    response_description="Returns the health status of the API",
)
async def health_check():
    """
    Perform a health check on the API.
    
    Returns:
        dict: A simple response indicating the API is operational.
    """
    return {"status": "healthy"} 