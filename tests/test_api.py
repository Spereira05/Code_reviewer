import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.crud.user import create_user
from app.schemas.user_schema import UserCreate
from app.models.user_model import User

@pytest.fixture(scope="function")
def test_user(test_db):
    # Create a test user
    user_in = UserCreate(
        email="test@example.com",
        username="testuser",
        password="testpassword"
    )
    user = create_user(db=test_db, user=user_in)
    return user

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to the AI Code Review API"

def test_create_user(client, test_db):
    response = client.post(
        "/api/users/",
        data={
            "email": "user@example.com",
            "username": "testuser2",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["username"] == "testuser2"
    assert "id" in data

def test_create_user_existing_email(client, test_user):
    response = client.post(
        "/api/users/",
        data={
            "email": "test@example.com",  # Same as test_user
            "username": "anothertestuser", 
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_create_user_existing_username(client, test_user):
    response = client.post(
        "/api/users/",
        data={
            "email": "another@example.com",
            "username": "testuser",  # Same as test_user
            "password": "testpassword"
        }
    )
    assert response.status_code == 400
    assert "Username already being used" in response.json()["detail"]

def test_login_user(client, test_user):
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_current_user(client, test_user):
    # First login to get token
    login_response = client.post(
        "/api/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword",
        },
    )
    token = login_response.json()["access_token"]
    
    # Use token to access protected endpoint
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"
    assert response.json()["email"] == "test@example.com"