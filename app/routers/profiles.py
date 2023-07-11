from fastapi import APIRouter, Depends, status, Query, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Profile
from app.services.security import (
    get_hashed_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.schemas.profiles import (
    ProfileResponseScheme,
    CreateProfileRequestScheme,
    TokenScheme,
)
from app.services.deps import get_current_user


router = APIRouter(prefix="/profiles", tags=["profiles"])


@router.post(
    "/",
    response_model=ProfileResponseScheme,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    db: Session = Depends(get_db), *, data: CreateProfileRequestScheme
):
    """Create new user"""
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


@router.post("/login", response_model=TokenScheme)
async def login(
    data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = db.query(Profile).filter_by(email=data.username).first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email",
        )
    hashed_pass = db_user.hashed_password

    if not verify_password(data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(db_user.email),
        "refresh_token": create_refresh_token(db_user.email),
    }


@router.get(
    "/",
    response_model=ProfileResponseScheme,
    dependencies=[Depends(get_current_user)],
)
def get_user(id: int = Query(None), db: Session = Depends(get_db)) -> Profile:
    return db.query(Profile).where(Profile.id == id).first()
