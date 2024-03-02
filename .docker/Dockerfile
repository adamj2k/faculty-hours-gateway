FROM python:3.11-slim
LABEL maintainer="adamj"

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1

RUN pip install poetry

COPY ./ /app/

RUN poetry config virtualenvs.create false \
    &&poetry install

CMD ["python3", "./main.py"]
