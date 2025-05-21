from sqlalchemy.orm import Session
from app.models.models import Submission, ReviewResults
from app.schemas.submission import SubmissionCreate, ReviewResultCreate

def get_submission(db: Session, submission_id: int):
    return db.query(Submission).filter(Submission.id == submission_id).first()

def get_user_submissions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Submission).filter(
        Submission.owner_id == user_id
    ).offset(skip).limit(limit).all()

def create_submission(db: Session, submission: SubmissionCreate, user_id: int, file_path: str):
    db_submission = Submission(
        file_name=submission.file_name,
        file_path=file_path,
        language=submission.language,
        status="PENDING",
        owner_id=user_id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission

def update_submission_status(db: Session, submission_id: int, status: str):
    db_submission = get_submission(db, submission_id)
    if db_submission:
        db_submission.status = status
        db.commit()
        db.refresh(db_submission)
    return db_submission

def create_review_result(db: Session, result: ReviewResultCreate):
    db_result = ReviewResults(
        agent_type=result.agent_type,
        feedback=result.feedback,
        submission_id=result.submission_id
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

def get_submission_results(db: Session, submission_id: int):
    return db.query(ReviewResults).filter(
        ReviewResults.submission_id == submission_id
    ).all()