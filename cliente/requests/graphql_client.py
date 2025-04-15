import requests
import json

# URL do servidor GraphQL
GRAPHQL_URL = "http://graphql.Dmgp.local"

def executar_query(query, variables=None):
    """
    Executa uma query ou mutation GraphQL no servidor.
    - query: A string da query ou mutation.
    - variables: Dicionário com as variáveis associadas (se necessário).
    """
    try:
        response = requests.post(GRAPHQL_URL, json={'query': query, 'variables': variables})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao comunicar com o servidor GraphQL: {e}")

def listar_livros():
    """Lista todos os livros no portfólio."""
    query = """
    query {
        tasks {
            id
            titulo
            descricao
            estado
        }
    }
    """
    resultado = executar_query(query)
    if resultado and 'data' in resultado:
        for livro in resultado['data']['tasks']:
            print(f"ID: {livro['id']}, Título: {livro['titulo']}, Estado: {livro['estado']}")
    else:
        print("Erro ao obter a lista de livros.")

def obter_livro(id_livro):
    """Obtém os detalhes de um livro específico pelo ID."""
    query = """
    query ($id: Int!) {
        task(id: $id) {
            id
            titulo
            descricao
            estado
        }
    }
    """
    variables = {'id': id_livro}
    resultado = executar_query(query, variables)
    if resultado and 'data' in resultado:
        livro = resultado['data']['task']
        if livro:
            print(f"ID: {livro['id']}, Título: {livro['titulo']}, Descrição: {livro['descricao']}, Estado: {livro['estado']}")
        else:
            print("Livro não encontrado.")
    else:
        print("Erro ao obter o livro.")

def adicionar_livro(id_livro, titulo, descricao, estado):
    """Adiciona um novo livro ao portfólio."""
    mutation = """
    mutation ($id: Int!, $titulo: String!, $descricao: String!, $estado: String!) {
        createTask(id: $id, titulo: $titulo, descricao: $descricao, estado: $estado) {
            task {
                id
                titulo
                descricao
                estado
            }
        }
    }
    """
    variables = {'id': id_livro, 'titulo': titulo, 'descricao': descricao, 'estado': estado}
    resultado = executar_query(mutation, variables)
    if resultado and 'data' in resultado:
        livro = resultado['data']['createTask']['task']
        print(f"Livro adicionado: ID: {livro['id']}, Título: {livro['titulo']}")
    else:
        print("Erro ao adicionar o livro.")

def atualizar_livro(id_livro, titulo=None, descricao=None, estado=None):
    """Atualiza os detalhes de um livro existente."""
    mutation = """
    mutation ($id: Int!, $titulo: String, $descricao: String, $estado: String) {
        updateTask(id: $id, titulo: $titulo, descricao: $descricao, estado: $estado) {
            task {
                id
                titulo
                descricao
                estado
            }
        }
    """
    variables = {'id': id_livro, 'titulo': titulo, 'descricao': descricao, 'estado': estado}
    resultado = executar_query(mutation, variables)
    if resultado and 'data' in resultado:
        livro = resultado['data']['updateTask']['task']
        print(f"Livro atualizado: ID: {livro['id']}, Título: {livro['titulo']}")
    else:
        print("Erro ao atualizar o livro.")

def eliminar_livro(id_livro):
    """Elimina um livro do portfólio pelo ID."""
    mutation = """
    mutation ($id: Int!) {
        deleteTask(id: $id) {
            ok
        }
    }
    """
    variables = {'id': id_livro}
    resultado = executar_query(mutation, variables)
    if resultado and 'data' in resultado:
        print(resultado['data']['deleteTask']['ok'])
    else:
        print("Erro ao eliminar o livro.")

if __name__ == "__main__":
    print("1. Listar livros")
    print("2. Obter livro")
    print("3. Adicionar livro")
    print("4. Atualizar livro")
    print("5. Eliminar livro")
    print("6. Sair")

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
            id_livro = int(input("ID do livro a atualizar: "))
            titulo = input("Novo título (ou deixe vazio): ") or None
            descricao = input("Nova descrição (ou deixe vazio): ") or None
            estado = input("Novo estado (ou deixe vazio): ") or None
            atualizar_livro(id_livro, titulo, descricao, estado)
        elif opcao == '5':
            id_livro = int(input("ID do livro a eliminar: "))
            eliminar_livro(id_livro)
        elif opcao == '6':
            print("A sair...")
            break
        else:
            print("Opção inválida!")