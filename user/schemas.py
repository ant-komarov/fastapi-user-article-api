from pydantic import BaseModel
from pydantic.v1 import ConfigDict


class UserBase(BaseModel):
    username: str
    age: int


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config(ConfigDict):
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
