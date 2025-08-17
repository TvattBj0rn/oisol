FROM ghcr.io/astral-sh/uv:0.1.37 AS uv

FROM python:3.12-slim AS python

WORKDIR /app
COPY . /app

ENV VIRTUAL_ENV=/opt/venv
RUN  \
    # we use a cache --mount to reuse the uv cache across builds
    --mount=type=cache,target=/root/.cache/uv \
    # we use a bind --mount to use the uv binary from the uv stage
    --mount=type=bind,from=uv,source=/uv,target=/uv \
    # we use a bind --mount to use the pyproject.toml from the host instead of adding a COPY layer
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    /uv venv /opt/venv && /uv pip install .

ENTRYPOINT ["sh", "/app/entrypoint.sh"]