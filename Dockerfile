FROM python:latest
VOLUME /home/ubuntu/oisol/data
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["sh", "/app/entrypoint.sh"]
