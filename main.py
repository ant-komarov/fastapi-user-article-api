from fastapi import FastAPI

from user.router import router as user_router
from article.router import router as article_router


app = FastAPI()

app.include_router(article_router)
app.include_router(user_router)


@app.get("/")
def root() -> dict:
    return {"message": "Hello!"}
