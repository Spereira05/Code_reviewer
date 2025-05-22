from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import Base, engine
from app.api.api import api_router
import os

# Import models to ensure they're registered with SQLAlchemy
from app.models import user_model, submission_model

# Only create tables when not in test mode
if not os.getenv("TESTING", "False").lower() in ("true", "1", "t"):
    try:
        # Create database tables
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Database connection error: {e}")
        print("Continuing startup without DB initialization...")

app = FastAPI(
    title="Code Review API",
    description="""
    AI-powered code review system using CrewAI agents.
    
    ## Features
    
    * Submit code files for analysis
    * Get feedback from multiple specialized AI agents
    * Receive quality, security, and performance recommendations
    
    ## Authentication
    
    * Create a user account:
        * JSON format: POST `/api/users/` with a JSON body
        * Form format: POST `/api/users/form` with form fields
    * Get JWT token: POST `/api/auth/token` (username/password as form fields)
    * Use token in Authorization header: `Bearer your_token_here`
    
    ## Account Creation
    
    For simple account creation, use the `/api/users/form` endpoint which shows form fields in the Swagger UI.
    """,
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to the AI Code Review API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
