ARG ENVIRONMENT="dev"
ARG PYTHON_VERSION="3.12"
ARG PORT=8000
FROM python:${PYTHON_VERSION}

WORKDIR /src


COPY pyproject.toml .
COPY poetry.lock .

RUN pip install poetry

RUN if [ "$ENVIRONMENT" = "prod" ]; then poetry install --no-dev; else poetry install --no-root; fi \
    && rm -rf ~/.cache/pypoetry/cache \
    && rm -rf ~/.cache/pypoetry/artifacts


COPY . .

RUN mv .env.example .env


EXPOSE $PORT

RUN poetry run yoyo apply migrations/
RUN uvicorn src.app:app  --port $PORT
