FROM python:3.10-alpine AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # skip compiling to .pyc files because container is ephemeral
    PYTHONDONTWRITEBYTECODE=1 \
    # ensure logs are written in real time
    PYTHONUNBUFFERED=1

WORKDIR /cpmonitor

FROM base as builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export --format requirements.txt \
    | /venv/bin/pip install --requirement /dev/stdin

COPY . .
RUN poetry build && /venv/bin/pip install dist/*.whl
