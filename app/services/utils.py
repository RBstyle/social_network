from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Depends
from fastapi.requests import Request

from app.db.models import Post, Profile
from app.db.database import get_db
from app.services.deps import get_current_user
from app.services.security import verify_password


async def get_post(post_id: int, db: Session):
    return db.query(Post).where(Post.id == post_id).first()


async def is_own_post(request: Request, post_id: int, db: Session) -> bool:
    current_user = await get_current_user(request=request, db=db)
    current_post = await get_post(post_id=post_id, db=db)

    return current_user.id == current_post.owner_id


async def check_post(request: Request, post_id: int, db: Session):
    if not await get_post(post_id=post_id, db=db):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if not await is_own_post(request=request, post_id=post_id, db=db):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't edit posts that aren't your own",
        )
    return None


def check_user(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(Profile).filter(Profile.email == username).first()
    if not user:
        return False
    if not verify_password(password=password, hashed_pass=user.hashed_password):
        return False
    return user
