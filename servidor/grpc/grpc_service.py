import os
import grpc
import jwt
import pika
import pymongo
from datetime import datetime
from concurrent import futures
import livros_pb2, livros_pb2_grpc

# Chave secreta para validar o JWT
JWT_SECRET = "segredo_super_secreto"
JWT_ALGORITHM = "HS256"

# MongoDB connection
mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
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


def validate_jwt(context):
    """Valida o JWT e devolve o payload se válido, ou termina a requisição."""
    metadata = dict(context.invocation_metadata())
    token = metadata.get('authorization')

    if not token or not token.startswith("Bearer "):
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token JWT ausente ou inválido.")

    try:
        jwt_token = token.split(" ")[1]
        payload = jwt.decode(jwt_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token expirado.")
    except jwt.InvalidTokenError:
        context.abort(grpc.StatusCode.UNAUTHENTICATED, "Token inválido.")


class LivroService(livros_pb2_grpc.LivroServiceServicer):
    def ListBooks(self, request, context):
        validate_jwt(context)
        books = list(collection.find({}, {"_id": 0}))
        return livros_pb2.ListBooksResponse(
            books=[livros_pb2.Book(**book) for book in books]
        )

    def GetBook(self, request, context):
        validate_jwt(context)
        book = collection.find_one({"id": request.id}, {"_id": 0})
        if book:
            return livros_pb2.Book(**book)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Livro não encontrado.")
        return livros_pb2.Book()

    def CreateBook(self, request, context):
        payload = validate_jwt(context)
        book_dict = {
            "id": request.book.id,
            "titulo": request.book.titulo,
            "descricao": request.book.descricao,
            "estado": request.book.estado
        }

        if collection.find_one({"id": book_dict["id"]}):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Já existe um livro com este ID.")
            return livros_pb2.OperationResponse(message="Erro ao criar livro.")

        collection.insert_one(book_dict)
        publish_log("create", book_dict["id"], payload["sub"])
        return livros_pb2.OperationResponse(message="Livro criado com sucesso.")

    def UpdateBook(self, request, context):
        payload = validate_jwt(context)
        result = collection.update_one(
            {"id": request.book.id},
            {"$set": {
                "titulo": request.book.titulo,
                "descricao": request.book.descricao,
                "estado": request.book.estado
            }}
        )
        if result.matched_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Livro não encontrado.")
            return livros_pb2.OperationResponse(message="Erro ao atualizar livro.")

        publish_log("update", request.book.id, payload["sub"])
        return livros_pb2.OperationResponse(message="Livro atualizado com sucesso.")

    def DeleteBook(self, request, context):
        payload = validate_jwt(context)
        result = collection.delete_one({"id": request.id})
        if result.deleted_count == 0:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Livro não encontrado.")
            return livros_pb2.OperationResponse(message="Erro ao eliminar livro.")

        publish_log("delete", request.id, payload["sub"])
        return livros_pb2.OperationResponse(message="Livro eliminado com sucesso.")


def serve():
    import grpc
    from concurrent import futures
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    livros_pb2_grpc.add_LivroServiceServicer_to_server(LivroService(), server)
    # Adiciona interceptor para CSP
    class CSPInterceptor(grpc.ServerInterceptor):
        def intercept_service(self, continuation, handler_call_details):
            def new_behavior(request, context):
                context.send_initial_metadata((('content-security-policy', "default-src 'self'"),))
                return continuation(handler_call_details).unary_unary(request, context)
            return grpc.unary_unary_rpc_method_handler(new_behavior)
    server.intercept_service(CSPInterceptor())
    server.add_insecure_port('[::]:55558')
    print("Servidor gRPC a correr na porta 55558...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()