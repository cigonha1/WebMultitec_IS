import grpc
from servidor.grpc import livros_pb2
from servidor.grpc import livros_pb2_grpc


def listar_livros(stub):
    """Lista todos os livros."""
    try:
        response = stub.ListBooks(livros_pb2.google_dot_protobuf_dot_empty__pb2.Empty())
        print("Livros disponíveis:")
        for livro in response.books:
            print(f"ID: {livro.id}, Título: {livro.titulo}, Estado: {livro.estado}")
    except grpc.RpcError as e:
        print(f"Erro ao listar livros: {e.details()}")


def obter_livro(stub, livro_id):
    """Obtém os detalhes de um livro específico."""
    try:
        response = stub.GetBook(livros_pb2.GetBookRequest(id=livro_id))
        print(f"ID: {response.id}, Título: {response.titulo}, Descrição: {response.descricao}, Estado: {response.estado}")
    except grpc.RpcError as e:
        print(f"Erro ao obter o livro: {e.details()}")


def adicionar_livro(stub, livro_id, titulo, descricao, estado):
    """Adiciona um novo livro."""
    try:
        livro = livros_pb2.Book(id=livro_id, titulo=titulo, descricao=descricao, estado=estado)
        response = stub.CreateBook(livros_pb2.BookRequest(book=livro))
        print(response.message)
    except grpc.RpcError as e:
        print(f"Erro ao adicionar o livro: {e.details()}")


def atualizar_livro(stub, livro_id, titulo, descricao, estado):
    """Atualiza os detalhes de um livro existente."""
    try:
        livro = livros_pb2.Book(id=livro_id, titulo=titulo, descricao=descricao, estado=estado)
        response = stub.UpdateBook(livros_pb2.BookRequest(book=livro))
        print(response.message)
    except grpc.RpcError as e:
        print(f"Erro ao atualizar o livro: {e.details()}")


def eliminar_livro(stub, livro_id):
    """Elimina um livro pelo ID."""
    try:
        response = stub.DeleteBook(livros_pb2.GetBookRequest(id=livro_id))
        print(response.message)
    except grpc.RpcError as e:
        print(f"Erro ao eliminar o livro: {e.details()}")


def main():
    # Conectar ao servidor gRPC
    channel = grpc.insecure_channel('localhost:55558')
    stub = livros_pb2_grpc.LivroServiceStub(channel)

    print("1. Listar livros")
    print("2. Obter livro")
    print("3. Adicionar livro")
    print("4. Atualizar livro")
    print("5. Eliminar livro")
    print("6. Sair")

    while True:
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listar_livros(stub)
        elif opcao == '2':
            livro_id = int(input("ID do livro: "))
            obter_livro(stub, livro_id)
        elif opcao == '3':
            livro_id = int(input("ID do novo livro: "))
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            estado = input("Estado: ")
            adicionar_livro(stub, livro_id, titulo, descricao, estado)
        elif opcao == '4':
            livro_id = int(input("ID do livro a atualizar: "))
            titulo = input("Novo título (ou deixe vazio): ") or None
            descricao = input("Nova descrição (ou deixe vazio): ") or None
            estado = input("Novo estado (ou deixe vazio): ") or None
            atualizar_livro(stub, livro_id, titulo, descricao, estado)
        elif opcao == '5':
            livro_id = int(input("ID do livro a eliminar: "))
            eliminar_livro(stub, livro_id)
        elif opcao == '6':
            print("A sair...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    main()