from sqlalchemy import Column, String, ForeignKey, Enum, Integer
from sqlalchemy.orm import relationship
from app.models.base_model import BaseDBModel

class Submission(BaseDBModel):
    __tablename__ = "submissions"

    file_path = Column(String)
    file_name = Column(String)
    language = Column(String)
    status = Column(Enum("PENDING", "PROCESSING", "COMPLETED", "FAILED", name="submission_status"))

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="submissions")
    review_results = relationship("ReviewResults", back_populates="submission")

class ReviewResults(BaseDBModel):
    __tablename__ = "review_results"

    agent_type = Column(String)
    feedback = Column(String)
    score = Column(Integer, default=0)

    submission_id = Column(Integer, ForeignKey("submissions.id"))
    submission = relationship("Submission", back_populates="review_results")