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


class UpdateProfileRequestScheme(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
