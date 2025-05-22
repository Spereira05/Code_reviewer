# Import all models to make them available from the models package
from app.models.user_model import User
from app.models.submission_model import Submission, ReviewResults
from app.models.base_model import BaseDBModel

__all__ = [
    "User",
    "Submission",
    "ReviewResults",
    "BaseDBModel"
]