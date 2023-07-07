from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Text,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship

from .database import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=func.now())
    hashed_password = Column(String)

    posts = relationship("Post")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
    )

    likes = relationship("Like")


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    user_id = Column(Integer, ForeignKey("profiles.id"))
    status = Column(Integer, default=1)
