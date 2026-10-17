FROM python:3.14-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never

WORKDIR /app

# Dependencies first (cached unless pyproject.toml or uv.lock change).
# sigurd's unused dependencies are skipped via `exclude-dependencies` in pyproject.toml.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --extra deploy --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --locked --no-dev --extra deploy --no-editable


FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

RUN useradd --create-home --uid 1000 app

# Only the virtualenv is needed: the package is installed in it, not used from the sources
COPY --from=builder /app/.venv /app/.venv

USER app
WORKDIR /home/app

EXPOSE 5011

# --preload loads the text once in the master process instead of once per worker
CMD ["gunicorn", "--bind", "0.0.0.0:5011", "--workers", "2", "--preload", "nibelungen_map_server.server_app:app"]
