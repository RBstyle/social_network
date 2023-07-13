from typing import Optional
from pydantic import BaseModel


class PostResponseScheme(BaseModel):
    owner_id: int
    title: Optional[str]
    content: str

    class Config:
        orm_mode = True


class ChangePostRequestScheme(BaseModel):
    title: Optional[str]
    content: str
