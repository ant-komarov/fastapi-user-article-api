FROM python:3.11.4-alpine
LABEL maintainer="anton_komarov_qa@ukr.net"

ENV PYTHONBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

# RUN apt-get update && apt-get -y install libpq-dev gcc bash
RUN pip install -r requirements.txt

COPY . .
