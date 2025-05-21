from pydantic import BaseModel
from datetime import datetime
from typing import List

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

class SubmissionBase(BaseModel):
    language: str
    file_name: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    status: str
    created_at: datetime
    file_path: str
    owner_id: int

    class Config:
        orm_mode = True

class SubmissionWithResults(Submission):
    review_results: List[ReviewResult] = []

    class Config:
        orm_mode = True