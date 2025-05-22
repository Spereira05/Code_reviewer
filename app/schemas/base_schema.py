from pydantic import BaseModel
from typing import Optional

class BaseSchema(BaseModel):
    """
    Base class for all Pydantic schemas in the application.
    This provides common settings and functionality.
    """
    class Config:
        orm_mode = True

class IDSchema(BaseSchema):
    """
    Base schema that includes an ID field.
    Used for responses that include database records.
    """
    id: Optional[int] = None