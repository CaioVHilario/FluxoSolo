from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from jwt import encode, decode, DecodeError
from http import HTTPStatus
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
from fluxosolo.core.settings import Settings
from fluxosolo.core.database import get_session
from fluxosolo.models.transactions import User

settings = Settings()
pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='auth/token'
)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plan_password: str, hash_password: str):
    return pwd_context.verify(plan_password, hash_password)


def creat_acces_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})

    encode_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encode_jwt


def get_current_user(
        session: Session = Depends(get_session),
        token: str = Depends(oauth2_scheme),
    ):
    
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject_email = payload.get('sub')

        if not subject_email:
            raise credentials_exception

    except DecodeError:
        raise credentials_exception

    user = session.scalar(
        select(User).where(User.email == subject_email)
    )

    if not user:
        raise credentials_exception

    return user
