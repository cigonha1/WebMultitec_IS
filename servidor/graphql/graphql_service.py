import os
import json
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, List, Field, Schema, Mutation
from pymongo import MongoClient
import pika
import datetime

# Caminho absoluto para o ficheiro de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'livros.json')


# Configurações MongoDB
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017/')
MONGO_DB = os.environ.get('MONGO_DB', 'biblioteca')
MONGO_COLLECTION = os.environ.get('MONGO_COLLECTION', 'livros')

# Configurações RabbitMQ
RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.environ.get('RABBITMQ_QUEUE', 'logs')


def get_mongo_collection():
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB]
    return db[MONGO_COLLECTION]


def log_to_rabbitmq(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
        channel.basic_publish(
            exchange='',
            routing_key=RABBITMQ_QUEUE,
            body=message.encode('utf-8'),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
    except Exception as e:
        print(f"Erro ao enviar log para RabbitMQ: {e}")


# Definir o modelo GraphQL para o Livro
class LivroType(ObjectType):
    id = Int()
    titulo = String()
    descricao = String()
    estado = String()


# Query para listar e obter livros
class Query(ObjectType):
    livros = List(LivroType)
    livro = Field(LivroType, id=Int(required=True))

    def resolve_livros(root, info):
        """Resolver para listar todos os livros."""
        return load_data()

    def resolve_livro(root, info, id):
        """Resolver para obter um livro específico pelo ID."""
        livros = load_data()
        return next((livro for livro in livros if livro["id"] == id), None)


# Função para carregar os dados
def load_data():
    collection = get_mongo_collection()
    return list(collection.find({}, {'_id': 0}))


# Mutation para criar, atualizar e eliminar livros
class CreateLivro(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String(required=True)
        descricao = String(required=True)
        estado = String(required=True)

    livro = Field(LivroType)

    def mutate(root, info, id, titulo, descricao, estado):
        collection = get_mongo_collection()
        if collection.find_one({'id': id}):
            raise Exception("Livro with this ID already exists")
        new_livro = {"id": id, "titulo": titulo, "descricao": descricao, "estado": estado}
        collection.insert_one(new_livro)
        log_to_rabbitmq(f"[{datetime.datetime.now()}] Livro criado: {new_livro}")
        return CreateLivro(livro=new_livro)


class UpdateLivro(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String()
        descricao = String()
        estado = String()

    livro = Field(LivroType)

    def mutate(root, info, id, titulo=None, descricao=None, estado=None):
        collection = get_mongo_collection()
        livro = collection.find_one({'id': id})
        if not livro:
            raise Exception("Livro not found")
        update_fields = {}
        if titulo is not None:
            update_fields['titulo'] = titulo
        if descricao is not None:
            update_fields['descricao'] = descricao
        if estado is not None:
            update_fields['estado'] = estado
        if update_fields:
            collection.update_one({'id': id}, {'$set': update_fields})
            livro.update(update_fields)
            log_to_rabbitmq(f"[{datetime.datetime.now()}] Livro atualizado: {livro}")
        return UpdateLivro(livro=livro)


class DeleteLivro(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = String()

    def mutate(root, info, id):
        collection = get_mongo_collection()
        livro = collection.find_one({'id': id})
        if not livro:
            raise Exception("Livro not found")
        collection.delete_one({'id': id})
        log_to_rabbitmq(f"[{datetime.datetime.now()}] Livro removido: {livro}")
        return DeleteLivro(ok="Livro deleted successfully")


# Definir as mutations no esquema
class Mutation(ObjectType):
    create_livro = CreateLivro.Field()
    update_livro = UpdateLivro.Field()
    delete_livro = DeleteLivro.Field()


# Criar o esquema
schema = Schema(query=Query, mutation=Mutation)

# Configurar a aplicação Flask
app = Flask(__name__)
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)  # graphiql=True para interface interativa
)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=55557, debug=True)