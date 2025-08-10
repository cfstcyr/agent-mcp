# source: https://docs.astral.sh/uv/guides/integration/docker/#intermediate-layers

ARG PYTHON_VERSION=3.13
ARG UV_VERSION=0.7.15

ARG PROJECT_CONF_DIR=./conf

FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv
FROM python:${PYTHON_VERSION} AS python-builder
FROM python:${PYTHON_VERSION}-slim AS python-executor

# ======== Install API dependencies using uv ========
# https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
FROM python-builder AS builder
COPY --from=uv /uv /uvx /bin/

WORKDIR /app

# Setup UV environment
ENV UV_PYTHON_DOWNLOADS=manual \
    UV_PYTHON_PREFERENCE=only-system \
    UV_LINK_MODE=copy

# Copy project files
COPY uv.lock pyproject.toml ./

# Fails if python version does not match
RUN uv python find --no-python-downloads > /dev/null

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable --no-dev  --compile-bytecode

# Copy source files
COPY . .

# Install project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable --no-dev --compile-bytecode


# ======== Build the base image ========
FROM python-executor AS base

ARG PROJECT_CONF_DIR

WORKDIR /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup --uid 1000 appuser

COPY --from=builder --chown=app:app \
    /app/.venv /app/.venv

COPY ${PROJECT_CONF_DIR} /app/conf/

ENV ENVIRONMENT=production

RUN chown -R appuser:appgroup /app
USER appuser


# ======= Build the application image ========
FROM base AS api
ENTRYPOINT ["/app/.venv/bin/api"]
