from fastapi import APIRouter
from app.api.endpoints import auth, users, submissions

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(users.router, prefix="/users")
api_router.include_router(submissions.router, prefix="/submissions")
