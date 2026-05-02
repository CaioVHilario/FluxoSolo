from fastapi import APIRouter, Depends, HTTPException
from http import HTTPStatus
from typing import Annotated
from sqlalchemy import select
from sqlalchemy.orm import Session

from fluxosolo.models.transactions import User
from fluxosolo.schemas import UserPublic, UserSchema, UserUpdate, Message
from fluxosolo.core.database import get_session
from fluxosolo.secrets import get_password_hash, get_current_user

router = APIRouter(prefix='/users', tags=['users'])
TSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post("/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: TSession):
    
    #porcura email e username no banco
    user_db = session.scalar(
        select(User).where(
            (User.email == user.email) | (User.username == user.username)
        )
    )

    #verificar se existe email e username no banco
    if user_db:
        if user_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username alredy exists',
            )
        elif user_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email alredy exists',
            )

    # faz o hash da senha
    password_hash = get_password_hash(user.password)
    user.password = password_hash

    # pega os dados inseridos pelo usuario e altera para bater com o schema do 
    # pydantic 
    user_db = User(**user.model_dump())

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.get('/me', response_model=UserPublic)
def read_current_user(current_user: CurrentUser):
    return current_user


@router.patch('/{user_id}', response_model=UserPublic)
def update_user(
    user_id: int,
    user: UserUpdate,
    session: TSession,
    current_user: CurrentUser
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='Not enough permissions'
        )
    
    user_db = session.scalar(
        select(User).where(User.id == current_user.id)
    )
    
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(user_db , key, value)

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@router.delete('/me', response_model=Message)
def delete_user(current_user: CurrentUser, session: TSession):
    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted'}
