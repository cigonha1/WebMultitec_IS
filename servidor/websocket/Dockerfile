# ./servidor/websocket/Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY websocket_server.py /app

RUN pip install --no-cache-dir fastapi uvicorn pika

CMD ["python", "websocket_server.py"]