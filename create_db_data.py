from fastapi import Depends
from sqlalchemy.orm import Session
from db import models
from db.dependencies import get_db
from passlib.hash import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


db = next(get_db())


def create_initial_data(session: Session):
    user1 = models.User(username="john", password=hash_password("john12345"), age=25)
    user2 = models.User(username="sam", password=hash_password("sam12345"), age=18)
    user3 = models.User(username="ben", password=hash_password("ben12345"), age=32)
    db.add(user1)
    db.add(user2)
    db.add(user3)

    db.commit()

    articles = [
        models.Article(text="Article 1", color="red", user_id=user1.id),
        models.Article(text="Article 2", color="blue", user_id=user1.id),
        models.Article(text="Article 3", color="green", user_id=user1.id),
        models.Article(text="Article 4", color="red", user_id=user1.id),
        models.Article(text="Article 5", color="green", user_id=user2.id),
        models.Article(text="Article 6", color="green", user_id=user2.id),
        models.Article(text="Article 7", color="red", user_id=user2.id),
        models.Article(text="Article 8", color="green", user_id=user2.id),
        models.Article(text="Article 9", color="green", user_id=user3.id),
        models.Article(text="Article 10", color="red", user_id=user3.id),
    ]
    for article in articles:
        db.add(article)

    db.commit()


if __name__ == "__main__":
    create_initial_data(session=db)
