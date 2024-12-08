from pydantic import BaseModel, Field, constr
from typing import Optional, List


class Token(BaseModel):
    token: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: constr(min_length=3)

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True
