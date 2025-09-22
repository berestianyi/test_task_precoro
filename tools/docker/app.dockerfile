FROM ghcr.io/astral-sh/uv:python3.12-alpine AS app

ARG UID=1000
ARG GID=1000

RUN apk add --no-cache \
    sudo \
    build-base \
    postgresql-dev \
    libpq \
  && addgroup -g ${GID} nonroot \
  && adduser -D -u ${UID} -G nonroot nonroot

USER nonroot

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

USER root

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

USER nonroot

COPY src/ /app/src
COPY tools/alembic /app/tools/alembic
