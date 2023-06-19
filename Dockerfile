FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN python -m pip install --upgrade pip \
    && pip install poetry
