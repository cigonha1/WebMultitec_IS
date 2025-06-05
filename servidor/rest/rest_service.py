import os
import jwt
import pika
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
from datetime import datetime

# Configs
JWT_SECRET = "segredo_super_secreto"
JWT_ALGORITHM = "HS256"

# Flask App
app = Flask(__name__)
api = Api(app)

# MongoDB connection
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

# RabbitMQ connection
rabbit_connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = rabbit_connection.channel()
channel.queue_declare(queue='livros.log')


def publish_log(action, book_id, user_id):
    message = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "book_id": book_id,
        "user_id": user_id
    }
    channel.basic_publish(exchange='', routing_key='livros.log', body=str(message))


def validate_jwt():
    auth_header = request.headers.get("Authorization", None)
    if not auth_header or not auth_header.startswith("Bearer "):
        return None, {"message": "Token JWT ausente ou inválido"}, 401
    try:
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload, None, None
    except jwt.ExpiredSignatureError:
        return None, {"message": "Token expirado"}, 401
    except jwt.InvalidTokenError:
        return None, {"message": "Token inválido"}, 401


class Livro(Resource):
    def get(self, livro_id=None):
        payload, err, code = validate_jwt()
        if err:
            return err, code

        if livro_id is None:
            livros = list(collection.find({}, {"_id": 0}))
            return jsonify(livros)
        livro = collection.find_one({"id": livro_id}, {"_id": 0})
        if livro:
            return jsonify(livro)
        return {"message": "Livro não encontrado"}, 404

    def post(self):
        payload, err, code = validate_jwt()
        if err:
            return err, code

        data = request.get_json()
        if collection.find_one({"id": data["id"]}):
            return {"message": "Já existe um livro com este ID"}, 400

        collection.insert_one(data)
        publish_log("create", data["id"], payload["sub"])
        return {"message": "Livro criado com sucesso"}, 201

    def put(self, livro_id):
        payload, err, code = validate_jwt()
        if err:
            return err, code

        data = request.get_json()
        result = collection.update_one({"id": livro_id}, {"$set": data})
        if result.matched_count == 0:
            return {"message": "Livro não encontrado"}, 404

        publish_log("update", livro_id, payload["sub"])
        return {"message": "Livro atualizado com sucesso"}

    def delete(self, livro_id):
        payload, err, code = validate_jwt()
        if err:
            return err, code

        result = collection.delete_one({"id": livro_id})
        if result.deleted_count == 0:
            return {"message": "Livro não encontrado"}, 404

        publish_log("delete", livro_id, payload["sub"])
        return {"message": "Livro eliminado com sucesso"}

@app.after_request
def add_csp_header(response):
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

# Rotas
api.add_resource(Livro, '/livros', '/livros/<int:livro_id>')

if __name__ == "__main__":
    app.run(host='192.168.246.33', port=55556)