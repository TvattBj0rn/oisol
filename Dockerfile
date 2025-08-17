# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,from=uv,source=/uv,target=/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv pip install .

# Copy the project into the image
ADD . /app

ENTRYPOINT ["sh", "/app/entrypoint.sh"]