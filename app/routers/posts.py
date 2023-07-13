from fastapi import APIRouter, Depends, Query, status
from fastapi.requests import Request
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Post
from app.services.deps import get_current_user
from app.services.utils import get_post, check_post
from app.schemas.posts import (
    PostResponseScheme,
    ChangePostRequestScheme,
)

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post(
    "/",
    response_model=PostResponseScheme,
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    request: Request,
    db: Session = Depends(get_db),
    *,
    data: ChangePostRequestScheme,
):
    """Create post"""
    current_user = await get_current_user(request=request, db=db)
    db_post = Post(
        owner_id=current_user.id,
        title=data.title,
        content=data.content,
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


@router.patch("/", dependencies=[Depends(get_current_user)])
async def edit_post(
    request: Request,
    post_id: int = Query(None),
    db: Session = Depends(get_db),
    *,
    data: ChangePostRequestScheme,
):
    error = await check_post(request=request, post_id=post_id, db=db)

    if error:
        raise error

    post_query = db.query(Post).filter(Post.id == post_id)
    update_data = data.dict(exclude_unset=True)
    post_query.filter(Post.id == post_id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(post_query.first())

    return {"status": "success", "note": post_query.first()}


@router.delete("/", dependencies=[Depends(get_current_user)])
async def delete_post(
    request: Request, post_id: int = Query(None), db: Session = Depends(get_db)
):
    error = await check_post(request=request, post_id=post_id, db=db)

    if error:
        raise error

    db_post = db.query(Post).filter(Post.id == post_id).first()
    db.delete(db_post)
    db.commit()
    return {"status": "success"}


@router.get("/", response_model=PostResponseScheme)
async def get_post_by_id(
    post_id: int = Query(None), db: Session = Depends(get_db)
) -> Post:
    return await get_post(post_id=post_id, db=db)
