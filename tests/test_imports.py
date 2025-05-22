import pytest

def test_import_core():
    """Test importing core app modules."""
    from app.main import app
    from app.api.api import api_router
    from app.db.session import Base, engine, get_db
    
    assert app is not None
    assert api_router is not None
    assert Base is not None
    assert engine is not None
    assert get_db is not None

def test_import_models():
    """Test importing models."""
    from app.models.user_model import User
    from app.models.submission_model import Submission, ReviewResults
    
    assert User is not None
    assert Submission is not None
    assert ReviewResults is not None

def test_import_schemas():
    """Test importing schemas."""
    from app.schemas.user_schema import UserCreate, User, Token, TokenData
    from app.schemas.submission_schema import SubmissionCreate, Submission, ReviewResult
    
    assert UserCreate is not None
    assert User is not None
    assert Token is not None
    assert TokenData is not None
    assert SubmissionCreate is not None
    assert Submission is not None
    assert ReviewResult is not None

def test_import_crud():
    """Test importing CRUD operations."""
    from app.crud.user import get_user, get_user_by_email, create_user
    from app.crud.submission import get_submission, create_submission
    
    assert get_user is not None
    assert get_user_by_email is not None
    assert create_user is not None
    assert get_submission is not None
    assert create_submission is not None

def test_import_endpoints():
    """Test importing API endpoints."""
    from app.api.endpoints.auth import router as auth_router
    from app.api.endpoints.users import router as users_router
    from app.api.endpoints.submissions import router as submissions_router
    
    assert auth_router is not None
    assert users_router is not None
    assert submissions_router is not None

def test_import_dependencies():
    """Test importing API dependencies."""
    from app.api.dependencies import get_current_user, create_access_token
    
    assert get_current_user is not None
    assert create_access_token is not None