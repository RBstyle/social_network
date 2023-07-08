from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.db.models import Post

from app.schemas.posts import (
    PostResponseScheme,
    ChangePostRequestScheme,
)

router = APIRouter(prefix="/posts", tags=["posts"])

"""As a user I need to be able to create, edit, delete and view posts"""


@router.post(
    "/",
    response_model=PostResponseScheme,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(db: Session = Depends(get_db), *, data: ChangePostRequestScheme):
    """Create post"""
    db_post = Post(
        owner_id=1,
        title=data.title,
        content=data.content,
    )  #!!!!!!!!!!
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch("/")
def edit_post(post_id: int = Query(None)):
    return f"edit post with id: {post_id}"


@router.delete("/")
def delete_post(post_id: int = Query(None)):
    return f"delete post with id: {post_id}"


@router.get("/", response_model=PostResponseScheme)
def get_post(post_id: int = Query(None), db: Session = Depends(get_db)) -> Post:
    return db.query(Post).where(Post.id == post_id).first()
