import os
import json
from concurrent import futures
import grpc

# Importar os ficheiros gerados pelo livros.proto
from servidor import livros_pb2
from servidor import livros_pb2_grpc

# Caminho absoluto para o ficheiro de dados
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'livros.json')


# Função para carregar os dados
def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


# Função para salvar os dados
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


# Implementação do serviço LivroService
class LivroService(livros_pb2_grpc.LivroServiceServicer):
    def ListBooks(self, request, context):
        """Lista todos os livros."""
        books = load_data()
        return livros_pb2.ListBooksResponse(
            books=[livros_pb2.Book(**book) for book in books]
        )

    def GetBook(self, request, context):
        """Obtém um livro específico pelo ID."""
        books = load_data()
        book = next((b for b in books if b["id"] == request.id), None)
        if book:
            return livros_pb2.Book(**book)
        context.set_code(grpc.StatusCode.NOT_FOUND)
        context.set_details("Livro não encontrado.")
        return livros_pb2.Book()

    def CreateBook(self, request, context):
        """Cria um novo livro."""
        books = load_data()
        new_book = {
            "id": request.book.id,
            "titulo": request.book.titulo,
            "descricao": request.book.descricao,
            "estado": request.book.estado,
        }

        # Verificar se o ID já existe
        if any(book["id"] == new_book["id"] for book in books):
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details("Já existe um livro com este ID.")
            return livros_pb2.OperationResponse(message="Falha ao criar o livro.")

        books.append(new_book)
        save_data(books)
        return livros_pb2.OperationResponse(message="Livro criado com sucesso.")

    def UpdateBook(self, request, context):
        """Atualiza um livro existente."""
        books = load_data()
        book = next((b for b in books if b["id"] == request.book.id), None)
        if not book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Livro não encontrado.")
            return livros_pb2.OperationResponse(message="Falha ao atualizar o livro.")

        # Atualizar os campos do livro
        book.update({
            "titulo": request.book.titulo,
            "descricao": request.book.descricao,
            "estado": request.book.estado,
        })
        save_data(books)
        return livros_pb2.OperationResponse(message="Livro atualizado com sucesso.")

    def DeleteBook(self, request, context):
        """Elimina um livro pelo ID."""
        books = load_data()
        book = next((b for b in books if b["id"] == request.id), None)
        if not book:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Livro não encontrado.")
            return livros_pb2.OperationResponse(message="Falha ao eliminar o livro.")

        books.remove(book)
        save_data(books)
        return livros_pb2.OperationResponse(message="Livro eliminado com sucesso.")


# Configuração e execução do servidor gRPC
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    livros_pb2_grpc.add_LivroServiceServicer_to_server(LivroService(), server)
    server.add_insecure_port('[::]:55558')
    print("Servidor gRPC a correr na porta 55558...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()