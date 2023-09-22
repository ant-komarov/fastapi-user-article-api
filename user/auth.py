from datetime import datetime, timedelta

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status

import settings
from db import models
from db.dependencies import get_db
from user.schemas import User, Token, UserCreate


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/sign-in")


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, raw_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(raw_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        validation_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY_JWT,
                algorithms=[settings.ALGORITHM]
            )
        except JWTError as ex:
            print(f"JWTError: {ex}")
            raise validation_exception

        user_data = payload.get("user")

        try:
            user = User.model_validate(user_data)
        except ValidationError:
            raise validation_exception

        return user

    @classmethod
    def create_token(cls, user: models.User) -> Token:
        user_data = User.model_validate(user)
        now = datetime.utcnow()

        payload = {
            "iat": now,
            "nbf": now,
            "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "sub": str(user_data.id),
            "user": user_data.model_dump()
        }

        token = jwt.encode(
            payload,
            settings.SECRET_KEY_JWT,
            algorithm=settings.ALGORITHM
        )

        return Token(access_token=token)

    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def register_user(self, user_data: UserCreate) -> Token:
        user = models.User(
            username=user_data.username,
            age=user_data.age,
            password=self.hash_password(user_data.password)
        )
        self.db.add(user)
        self.db.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        validation_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={
                "WWW-Authenticate": "Bearer"
            }
        )
        user = self.db.query(models.User).filter(models.User.username == username).first()

        if not user or not self.verify_password(password, user.password):
            raise validation_exception

        return self.create_token(user)
