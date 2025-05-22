from pydantic import EmailStr
from typing import Optional
from app.schemas.base_schema import BaseSchema, IDSchema

class UserBase(BaseSchema):
    email: str
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase, IDSchema):
    pass

class UserInDB(UserBase, IDSchema):
    hashed_password: str

class Token(BaseSchema):
    access_token: str
    token_type: str

class TokenData(BaseSchema):
    username: Optional[str] = None