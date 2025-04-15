from zeep import Client

# URL do WSDL do servidor SOAP
WSDL_URL = 'http://soap.Dmgp.local/?wsdl'
client = Client(WSDL_URL)

def listar_livros():
    """Lista todos os livros."""
    try:
        livros = client.service.list_livros()
        for livro in livros:
            print(f"ID: {livro['id']}, Título: {livro['titulo']}, Estado: {livro['estado']}")
    except Exception as e:
        print(f"Erro ao listar livros: {e}")

def obter_livro(id_livro):
    """Obtém um livro específico pelo ID."""
    try:
        livro = client.service.get_livro(id_livro)
        print(f"Livro ID {id_livro}: Título: {livro['titulo']}, Estado: {livro['estado']}")
    except Exception as e:
        print(f"Erro ao obter o livro: {e}")

def adicionar_livro(id_livro, titulo, descricao, estado):
    """Adiciona um novo livro ao portfólio."""
    try:
        resposta = client.service.create_livro({'id': id_livro, 'titulo': titulo, 'descricao': descricao, 'estado': estado})
        print(f"Servidor: {resposta}")
    except Exception as e:
        print(f"Erro ao adicionar o livro: {e}")

def eliminar_livro(id_livro):
    """Remove um livro do portfólio pelo ID."""
    try:
        resposta = client.service.delete_livro(id_livro)
        print(f"Servidor: {resposta}")
    except Exception as e:
        print(f"Erro ao eliminar o livro: {e}")

if __name__ == "__main__":
    print("1. Listar livros\n2. Obter livro\n3. Adicionar livro\n4. Eliminar livro\n5. Sair")
    while True:
        opcao = input("Escolha uma opção: ")
        if opcao == '1':
            listar_livros()
        elif opcao == '2':
            id_livro = int(input("ID do livro: "))
            obter_livro(id_livro)
        elif opcao == '3':
            id_livro = int(input("ID do novo livro: "))
            titulo = input("Título: ")
            descricao = input("Descrição: ")
            estado = input("Estado: ")
            adicionar_livro(id_livro, titulo, descricao, estado)
        elif opcao == '4':
            id_livro = int(input("ID do livro a eliminar: "))
            eliminar_livro(id_livro)
        elif opcao == '5':
            print("A sair...")
            break
        else:
            print("Opção inválida!")