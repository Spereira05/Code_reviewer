import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_read_main():
    """Basic smoke test to check if the app is running."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_api_router_availability():
    """Check if API router endpoints are mounted."""
    response = client.get("/api/docs")
    # Just checking for a response, even if it's a redirect or error
    assert response.status_code != 500

def test_api_versioning():
    """Ensure API versioning structure is working."""
    response = client.get("/api")
    # Should get something other than a 500 server error
    assert response.status_code != 500

def test_import_modules():
    """Test that we can import key modules."""
    # These imports should not raise exceptions
    from app.db.session import Base, get_db
    from app.api.api import api_router
    from app.models.models import User, Submission
    
    assert Base is not None
    assert get_db is not None 
    assert api_router is not None
    assert User is not None
    assert Submission is not None