from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str 

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool 

    class Config:
        orm_mode = True

class SubmissionBase(BaseModel):
    language: str
    file_name: str 

class submissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    status: str
    create_at: datetime
    file_path: str
    owner_id: int

    class Config:
        orm_mode = True 

class ReviewResultBase(BaseModel):
    agent_type: str
    feedback: str

class ReviewResultCreate(ReviewResultBase):
    submission_id: int

class ReviewResult(ReviewResultBase):
    id: int
    created_at: datetime
    submission_id: int 
    
    class Config:
        orm_mode = True

class SubmissionWithResults(Submission):
    review_results: List[ReviewResult] = []

    class Config:
        orm_mode = True

# Token schema for authentication
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
