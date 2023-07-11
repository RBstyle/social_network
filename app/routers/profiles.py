from fastapi import APIRouter, Depends, status, Query, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.database import get_db
from app.db.models import Profile
from app.services.security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    get_hashed_password,
    create_access_token,
)
from app.schemas.profiles import (
    ProfileResponseScheme,
    CreateProfileRequestScheme,
    TokenScheme,
)
from app.services.deps import get_current_user
from app.services.utils import check_user

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
def login_for_access_token(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = check_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/",
    response_model=ProfileResponseScheme,
    dependencies=[Depends(get_current_user)],
)
def get_user(id: int = Query(None), db: Session = Depends(get_db)) -> Profile:
    return db.query(Profile).where(Profile.id == id).first()
