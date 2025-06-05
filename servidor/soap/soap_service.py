import os
import jwt
import pika
from spyne import Application, rpc, ServiceBase, Integer, Unicode, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from pymongo import MongoClient
from datetime import datetime
from wsgiref.simple_server import make_server

# Importações dos módulos de exportação/importação
from exportar_json import exportar_json
from importar_json import importar_json
from exportar_xml import exportar_xml
from importar_xml import importar_xml

# Configurações
JWT_SECRET = "segredo_super_secreto"
JWT_ALGORITHM = "HS256"

# MongoDB
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

# RabbitMQ
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


# Modelo de Livro
class LivroModel(ComplexModel):
    id = Integer
    titulo = Unicode
    descricao = Unicode
    estado = Unicode


# Serviço SOAP
class LivroService(ServiceBase):

    def _validate_jwt(ctx):
        auth = ctx.transport.req_env.get("HTTP_AUTHORIZATION")
        if not auth or not auth.startswith("Bearer "):
            raise ValueError("Token JWT ausente ou inválido")
        token = auth.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token expirado")
        except jwt.InvalidTokenError:
            raise ValueError("Token inválido")

    @rpc(_returns=Array(LivroModel))
    def list_livros(ctx):
        # Adiciona o header CSP à resposta SOAP
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        livros = list(collection.find({}, {"_id": 0}))
        return livros

    @rpc(Integer, _returns=LivroModel)
    def get_livro(ctx, livro_id):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        livro = collection.find_one({"id": livro_id}, {"_id": 0})
        if livro:
            return livro
        raise ValueError("Livro não encontrado")

    @rpc(LivroModel, _returns=Unicode)
    def create_livro(ctx, livro):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        payload = LivroService._validate_jwt(ctx)
        if collection.find_one({"id": livro.id}):
            raise ValueError("Já existe livro com este ID")
        doc = {
            "id": livro.id,
            "titulo": livro.titulo,
            "descricao": livro.descricao,
            "estado": livro.estado
        }
        collection.insert_one(doc)
        publish_log("create", livro.id, payload["sub"])
        return "Livro criado com sucesso"

    @rpc(Integer, LivroModel, _returns=Unicode)
    def update_livro(ctx, livro_id, livro):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        payload = LivroService._validate_jwt(ctx)
        result = collection.update_one({"id": livro_id}, {"$set": {
            "titulo": livro.titulo,
            "descricao": livro.descricao,
            "estado": livro.estado
        }})
        if result.matched_count == 0:
            raise ValueError("Livro não encontrado")
        publish_log("update", livro_id, payload["sub"])
        return "Livro atualizado com sucesso"

    @rpc(Integer, _returns=Unicode)
    def delete_livro(ctx, livro_id):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        payload = LivroService._validate_jwt(ctx)
        result = collection.delete_one({"id": livro_id})
        if result.deleted_count == 0:
            raise ValueError("Livro não encontrado")
        publish_log("delete", livro_id, payload["sub"])
        return "Livro eliminado com sucesso"

    # Métodos para exportação/importação
    @rpc(_returns=Unicode)
    def exportar_json_rpc(ctx):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        exportar_json()
        return "Exportação JSON concluída."

    @rpc(_returns=Unicode)
    def importar_json_rpc(ctx):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        importar_json()
        return "Importação JSON concluída."

    @rpc(_returns=Unicode)
    def exportar_xml_rpc(ctx):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        exportar_xml()
        return "Exportação XML concluída."

    @rpc(_returns=Unicode)
    def importar_xml_rpc(ctx):
        ctx.transport.resp_headers['Content-Security-Policy'] = "default-src 'self'"
        _ = LivroService._validate_jwt(ctx)
        importar_xml()
        return "Importação XML concluída."


# Configuração do servidor SOAP
application = Application(
    [LivroService],
    tns='soap.livros',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    print("SOAP service running on http://0.0.0.0:55555")
    server = make_server('0.0.0.0', 55555, wsgi_app)
    server.serve_forever()