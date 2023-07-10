from sqlalchemy.orm import Session

from app.db.models import Post


async def get_post(post_id: int, db: Session):
    return db.query(Post).where(Post.id == post_id).first()
