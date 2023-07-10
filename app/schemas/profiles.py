from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class ProfileResponseScheme(BaseModel):
    email: str
    first_name: str
    last_name: Optional[str] = None
    created_at: datetime

    class Config:
        orm_mode = True


class CreateProfileRequestScheme(BaseModel):
    email: str
    first_name: str
    last_name: Optional[str] = None
    password: str


class TokenScheme(BaseModel):
    access_token: str
    refresh_token: str


class UpdateProfileRequestScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class UserOut(BaseModel):
    id: int
    email: str


class SystemUser(UserOut):
    password: str
