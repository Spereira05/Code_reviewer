import os
from typing import List
import uuid
import shutil 
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.submission import Submission, SubmissionCreate
from app.api.dependencies import get_current_user
from app.schemas.user import User
from app.crud import submission as crud_submission
from app.ai.process import process_submission

router = APIRouter(tags=["submissions"])

UPLOAD_DIR ="uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=Submission)
async def create_submission(
    language: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    filename = file.filename
    file_path = f"{UPLOAD_DIR}/{uuid.uuid4()}_{filename}"
    
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    submission_data = SubmissionCreate(
        language=language,
        file_name=filename
    )a
    submission = crud_submission.create_submission(
        db=db,
        submission=submission_data,
        user_id=current_user.id,
        file_path=file_path
    )
    background_tasks.add_task(
        process_submission,
        submission_id=submission.id,
        file_path=file_path,
        db=db
    )
    return submission

@router.get("/", response_model=List[Submission])
def read_submissions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    submissions = crud_submission.get_user_submissions(db, user_id=current_user.id, skip=skip, limit=limit)
    return submissions

def read_submission(
        submission_id: int,
        db: Session = Depends(get_db),
        currents_user
