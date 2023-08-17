from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.services.security import ALGORITHM, JWT_SECRET_KEY
from app.schemas.profiles import TokenPayload, UserOut
from app.db.database import get_db
from app.db.models import Profile


reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/profiles/login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(reuseable_oauth),
    db: Session = Depends(get_db),
    request: Request = None,
) -> UserOut:
    if request:
        token = request.cookies.get("access_token")

        if not token:
            return

        if "Bearer" in token:
            token: str = token.split("Bearer")[1].strip()

    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    db_user = db.query(Profile).filter_by(email=token_data.sub).first()

    if db_user:
        sys_user = UserOut(
            id=db_user.id,
            email=db_user.email,
            password=db_user.hashed_password,
        )

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
        )

    return sys_user
