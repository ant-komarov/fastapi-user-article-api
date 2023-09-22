from sqlalchemy.orm import Session

from article import schemas
from db import models


def get_articles(db: Session):
    return db.query(models.Article)


def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(
        text=article.text, color=article.color, user_id=article.user_id
    )
    db.add(db_article)
    db.commit()
    db.refresh(db_article)

    return db_article
