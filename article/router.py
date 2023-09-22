from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from article import schemas, crud
from db.dependencies import get_db
from db.models import User
from user.auth import get_current_user

router = APIRouter(prefix="/articles")


@router.post("/", response_model=schemas.ArticleRead)
def create_article(
    article: schemas.ArticleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return crud.create_article(db=db, article=article)


@router.get("/", response_model=List[schemas.ArticleRead])
def get_all_articles(
    db: Session = Depends(get_db), user: User = Depends(get_current_user)
):
    return crud.get_articles(db=db)
