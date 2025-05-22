from sqlalchemy import Column, Integer
from app.db.session import Base

class BaseDBModel(Base):
    """
    Base class for all SQLAlchemy models in the application.
    This provides common fields and functionality.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)