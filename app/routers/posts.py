from fastapi import APIRouter, Depends, Query, status, HTTPException
from fastapi.requests import Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Post
from app.services.deps import get_current_user
from app.services.utils import get_post

from app.db.models import Profile
from app.schemas.posts import (
    PostResponseScheme,
    ChangePostRequestScheme,
)

router = APIRouter(prefix="/posts", tags=["posts"])

"""As a user I need to be able to create, edit, delete and view posts"""


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


@router.patch(
    "/",
    dependencies=[Depends(get_current_user)],
)
async def edit_post(
    request: Request,
    post_id: int = Query(None),
    db: Session = Depends(get_db),
    *,
    data: ChangePostRequestScheme,
):
    current_user = await get_current_user(request=request, db=db)
    current_post = await get_post(post_id=post_id, db=db)

    if current_user.id == current_post.owner_id:
        post_query = db.query(Post).filter(Post.id == post_id)
        update_data = data.dict(exclude_unset=True)
        post_query.filter(Post.id == post_id).update(
            update_data, synchronize_session=False
        )
        db.commit()
        db.refresh(current_post)

    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't edit posts that aren't your own",
        )

    return {"status": "success", "note": current_post}


@router.delete("/")
def delete_post(post_id: int = Query(None)):
    return f"delete post with id: {post_id}"


@router.get("/", response_model=PostResponseScheme)
async def get_post_by_id(
    post_id: int = Query(None), db: Session = Depends(get_db)
) -> Post:
    return await get_post(post_id=post_id, db=db)
