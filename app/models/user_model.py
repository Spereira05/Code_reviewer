from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.models.base_model import BaseDBModel

class User(BaseDBModel):
    __tablename__ = "users"
    
    username = Column(String)
    password = Column(String)
    email = Column(String, unique=True, index=True)
    
    submissions = relationship("Submission", back_populates="owner")