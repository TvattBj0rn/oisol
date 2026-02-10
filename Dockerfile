FROM python:3.13.12-slim
LABEL authors="Vask"
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
COPY . /app
RUN uv sync
ENTRYPOINT ["uv", "run", "main.py"]