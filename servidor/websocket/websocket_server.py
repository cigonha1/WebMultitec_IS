import json
import asyncio
import pika
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

# Lista de WebSocket ativos
active_connections = []

# Permitir chamadas CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    print("Cliente WebSocket conectado.")
    try:
        while True:
            await websocket.receive_text()  # manter a ligação
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print("Cliente WebSocket desconectado.")

# Função para enviar mensagens a todos os clientes WebSocket
async def broadcast(message):
    disconnected = []
    for connection in active_connections:
        try:
            await connection.send_text(message)
        except:
            disconnected.append(connection)
    for conn in disconnected:
        active_connections.remove(conn)

# Listener do RabbitMQ em thread separada
def rabbitmq_listener():
    def callback(ch, method, properties, body):
        message = body.decode()
        print("Nova mensagem RabbitMQ:", message)
        asyncio.run(broadcast(message))

    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()
    channel.queue_declare(queue="livros.log")
    channel.basic_consume(queue="livros.log", on_message_callback=callback, auto_ack=True)
    print("🟢 WebSocket server a escutar RabbitMQ...")
    channel.start_consuming()

# Iniciar listener RabbitMQ em paralelo
threading.Thread(target=rabbitmq_listener, daemon=True).start()

if __name__ == "__main__":
    uvicorn.run(app, host="198.168.246.33", port=8000)