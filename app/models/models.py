from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from app.db.session import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    submissions = relationship("Submission", back_populates="owner")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String)
    file_path = Column(String)
    language = Column(String)
    status = Column(Enum("PENDING", "PROCESSING", "COMPLETED", "FAILED", name="submission_status"))
    created_at = Column(DateTime, server_default=func.now())

    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = realtionship("User", back_populates="submissions")
    review_results = relationship("ReviewResults", back_populates="submission")

class ReviewResults(Base):
    __tablename__ = "review_results"

    id = Column(Integer, primary_key=True, index=True)
    agent_type = Column(String)
    feedback = Column(String)
    created_at = Column(DateTime, server_default=func.now())

    submission_id = Column(Integer, ForeignKey("submissions.id"))
    submission = relationship("Submission", back_populates="review_results")
