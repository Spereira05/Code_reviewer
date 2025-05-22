from typing import List
from app.schemas.base_schema import BaseSchema, IDSchema

class ReviewResultBase(BaseSchema):
    agent_type: str
    feedback: str
    score: int = 0

class ReviewResultCreate(ReviewResultBase):
    pass

class ReviewResult(ReviewResultBase, IDSchema):
    submission_id: int

class SubmissionBase(BaseSchema):
    language: str
    file_name: str

class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase, IDSchema):
    status: str
    file_path: str
    owner_id: int

class SubmissionWithResults(Submission):
    review_results: List[ReviewResult] = []