# build frontend
FROM node:19-alpine AS frontend-builder

WORKDIR /cpmonitor

COPY package.json .
COPY cpmonitor/static/css cpmonitor/static/css
RUN yarn install && \
    yarn run compile:css

# basic python settings
FROM python:3.10-alpine AS python-base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    # skip compiling to .pyc files because container is ephemeral
    PYTHONDONTWRITEBYTECODE=1 \
    # ensure logs are written in real time
    PYTHONUNBUFFERED=1

WORKDIR /cpmonitor

# build python app
FROM python-base as python-builder

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.3.2

RUN pip install "poetry==$POETRY_VERSION"
RUN python -m venv /venv

COPY pyproject.toml poetry.lock ./
RUN poetry export --without dev --format requirements.txt \
    | /venv/bin/pip install --requirement /dev/stdin

COPY . .
COPY --from=frontend-builder /cpmonitor/cpmonitor/static/css ./cpmonitor/static/css
COPY --from=frontend-builder /cpmonitor/node_modules/bootstrap/dist/js ./node_modules/bootstrap/dist/js
COPY --from=frontend-builder /cpmonitor/node_modules/jquery/dist ./node_modules/jquery/dist
RUN /venv/bin/python manage.py collectstatic --no-input -v 2 --settings=config.settings.container
RUN poetry build && \
    /venv/bin/pip install dist/*.whl

# put together final app container
FROM python-base as final

ENV PATH="/venv/bin:${PATH}"
ENV VIRTUAL_ENV="/venv"

# run as unprivileged user instead of root
RUN adduser -D user
USER user

EXPOSE 8000

COPY --from=python-builder /venv /venv
COPY --from=python-builder /static /static
COPY config/nginx /nginx/conf.d

CMD ["gunicorn", "--log-level", "debug", "--bind", ":8000", "--workers", "3", "config.wsgi:application"]