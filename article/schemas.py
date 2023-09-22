from pydantic import BaseModel
from pydantic.v1 import ConfigDict

from db.models import Color
from user.schemas import User


class ArticleBase(BaseModel):
    text: str
    color: Color


class ArticleCreate(ArticleBase):
    user_id: int


class ArticleRead(ArticleBase):
    id: int
    user: User

    class Config(ConfigDict):
        from_attributes = True
