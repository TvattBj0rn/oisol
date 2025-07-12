FROM python:3.12
WORKDIR /app
COPY . /app
RUN pip install uv && uv pip install .
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
