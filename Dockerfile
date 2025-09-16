FROM python:3.13
WORKDIR /app
COPY . /app
RUN pip install .
ENTRYPOINT ["sh", "/app/entrypoint.sh"]