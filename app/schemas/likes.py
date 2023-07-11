from pydantic import BaseModel


class LikeResponseScheme(BaseModel):
    post_id: int
    status: int

    class Config:
        orm_mode = True


class ChangeLikeRequestScheme(BaseModel):
    status: int
