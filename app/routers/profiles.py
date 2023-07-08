from fastapi import APIRouter, Depends, status, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Profile
from app.services.security import get_hashed_password
from app.schemas.profiles import (
    ProfileResponseScheme,
    CreateProfileRequestScheme,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "/",
    response_model=ProfileResponseScheme,
    status_code=status.HTTP_201_CREATED,
)
async def create_profile(
    db: Session = Depends(get_db), *, data: CreateProfileRequestScheme
):
    """Create user in database"""
    user = db.query(Profile).filter_by(email=data.email).all()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist",
        )
    db_user = Profile(
        email=data.email.lower(),
        first_name=data.first_name,
        last_name=data.last_name,
        hashed_password=get_hashed_password(data.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/", response_model=ProfileResponseScheme)
def get_user(id: int = Query(None), db: Session = Depends(get_db)) -> Profile:
    return db.query(Profile).where(Profile.id == id).first()
