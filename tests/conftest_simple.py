import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure app directory is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Set testing mode
os.environ["TESTING"] = "True"

# Import app after setting testing mode
from app.main import app

@pytest.fixture
def client():
    """Return a test client for the app."""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_environment():
    """Setup the test environment."""
    # Save original env vars
    original_env = {}
    for key in ['DATABASE_URL', 'TESTING']:
        if key in os.environ:
            original_env[key] = os.environ[key]
    
    # Set test environment variables
    os.environ["TESTING"] = "True"
    os.environ["DATABASE_URL"] = "sqlite:///./test.db"
    
    yield
    
    # Restore original env vars
    for key in original_env:
        os.environ[key] = original_env[key]
    
    # Remove keys that weren't there before
    for key in ['DATABASE_URL', 'TESTING']:
        if key not in original_env and key in os.environ:
            del os.environ[key]