from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import EmailStr

from app.api.dependencies import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import User as UserSchema, UserCreate
from app.crud import user as crud_user
from app.db.session import get_db 

router = APIRouter(tags=["Users"])

@router.post("/", response_model=UserSchema)
def create_user(
    email: EmailStr = Form(...),
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Create user
    user_data = UserCreate(email=email, username=username, password=password)
        
    # Check if email already exists
    db_user_email = crud_user.get_user_by_email(db, email=user_data.email)
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    # Check if username already exists
    db_user_username = crud_user.get_user_by_username(db, username=user_data.username)
    if db_user_username:
        raise HTTPException(status_code=400, detail="Username already being used")
        
    # Create the user
    return crud_user.create_user(db=db, user=user_data)

@router.get("/me", response_model=UserSchema)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
