from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.requests import Request

from app.services.deps import get_current_user
from app.services.utils import get_post, is_own_post
from app.schemas.likes import LikeResponseScheme, ChangeLikeRequestScheme
from app.db.models import Like
from app.db.database import get_db

router = APIRouter(
    prefix="/likes", tags=["likes"], dependencies=[Depends(get_current_user)]
)


@router.post("/", response_model=LikeResponseScheme)
async def evaluate(
    request: Request,
    post_id: int = Query(None),
    db: Session = Depends(get_db),
    *,
    data: ChangeLikeRequestScheme,
):
    if not await get_post(post_id=post_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if await is_own_post(request=request, post_id=post_id, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't like your's posts",
        )

    current_user = await get_current_user(request=request, db=db)
    db_like = Like(
        post_id=post_id,
        user_id=current_user.id,
        status=data.status,
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like
