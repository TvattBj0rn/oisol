FROM python:3.13
WORKDIR /app
COPY . /app
RUN uv sync
ENTRYPOINT ["sh", "/app/entrypoint.sh"]