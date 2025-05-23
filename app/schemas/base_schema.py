from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseSchema(BaseModel):
    """
    Base class for all Pydantic schemas in the application.
    This provides common settings and functionality.
    """
    model_config = ConfigDict(from_attributes=True)

class IDSchema(BaseSchema):
    """
    Base schema that includes an ID field.
    Used for responses that include database records.
    """
    id: Optional[int] = None