# Fastapi-user-article-api

## Run using docker

Docker must be already installed

```shell
git clone https://github.com/ant-komarov/fastapi-user-article-api
cd fastapi-user-article-api
docker-compose up --build
```

## Testing (Pytest)

For running pytest change _DATABASE_URL_ in **settings.py** and _sqlalchemy.url_ in **alembic.ini**
```shell
pytest
```

## Testing endpoints using Postman

- Import collection **User-article-api.postman_collection.json** into Postman
- Use /users/sign-up endpoint to add new user and receive token
- Or use /users/sign-in endpoint to receive token using credentials:
_username_: **john**, _password_: **john12345**
- To access endpoints: GET /articles, POST /articles, GET /users in header **Authorization** add **Bearer {your token}**

Also can be used Swagger documentation at http://127.0.0.1:8000/docs

## Technologies used

Fast API, SQLAlchemy + Alembic, PostgreSQL, Docker
