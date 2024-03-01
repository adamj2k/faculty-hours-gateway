FROM python:3.11-slim
LABEL maintainer="adamj"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock /app/
COPY ./ /app/
COPY ./README.md /app/

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python3", "./main.py"]
