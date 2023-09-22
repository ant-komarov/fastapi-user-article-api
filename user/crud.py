from sqlalchemy import func
from sqlalchemy.orm import Session

from db.models import Color, User, Article


def get_users(
    db: Session, age: int = None, color: Color = None, articles_num: int = None
):
    queryset = db.query(User)
    if age:
        queryset = queryset.filter(User.age > age)
    if color:
        queryset = queryset.join(Article, User.id == Article.user_id).filter(
            Article.color == color
        )
    if articles_num:
        queryset = (
            queryset.join(Article, User.id == Article.user_id)
            .group_by(User.id, User.username, User.password, User.age)
            .having(func.count(Article.id) > articles_num)
        )
    return queryset
