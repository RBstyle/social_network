from sqlalchemy.orm import Session

from app.db.models import Post
from app.services.deps import get_current_user


async def get_post(post_id: int, db: Session):
    return db.query(Post).where(Post.id == post_id).first()


async def is_own_post(request, post_id, db) -> bool:
    current_user = await get_current_user(request=request, db=db)
    current_post = await get_post(post_id=post_id, db=db)

    return current_user.id == current_post.owner_id
