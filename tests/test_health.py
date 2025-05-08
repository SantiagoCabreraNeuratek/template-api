"""
Tests for the health endpoint.
"""
from fastapi.testclient import TestClient

from app.core.config import settings
from main import app

client = TestClient(app)


def test_health_check():
    """
    Test health check endpoint returns 200 OK.
    """
    response = client.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"} 