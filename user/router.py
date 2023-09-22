from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.dependencies import get_db
from db.models import Color, User
from user import schemas, crud
from user.auth import AuthService, get_current_user

router = APIRouter(prefix="/users")


@router.post("/sign-up", response_model=schemas.Token)
def sign_up(
        user: schemas.UserCreate,
        service: AuthService = Depends()
):
    return service.register_user(user)


@router.post("/sign-in", response_model=schemas.Token)
def sign_in(
        form: OAuth2PasswordRequestForm = Depends(),
        service: AuthService = Depends()
):
    return service.authenticate_user(
        form.username,
        form.password
    )


@router.get("/", response_model=List[schemas.User])
def get_users(
        age: int | None = None,
        color: Color | None = None,
        articles_num: int | None = None,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return crud.get_users(db=db, age=age, color=color, articles_num=articles_num)
