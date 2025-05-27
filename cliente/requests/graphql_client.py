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
        livros {
            id
            titulo
            descricao
            estado
        }
    }
    """
    resultado = executar_query(query)
    if resultado and 'data' in resultado:
        for livro in resultado['data']['livros']:
            print(f"ID: {livro['id']}, Título: {livro['titulo']}, Estado: {livro['estado']}")
    else:
        print("Erro ao obter a lista de livros.")

def obter_livro(id_livro):
    """Obtém os detalhes de um livro específico pelo ID."""
    query = """
    query ($id: Int!) {
        livro(id: $id) {
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
        livro = resultado['data']['livro']
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
        createLivro(id: $id, titulo: $titulo, descricao: $descricao, estado: $estado) {
            livro {
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
        livro = resultado['data']['createLivro']['livro']
        print(f"Livro adicionado: ID: {livro['id']}, Título: {livro['titulo']}")
    else:
        print("Erro ao adicionar o livro.")

def atualizar_livro(id_livro, titulo=None, descricao=None, estado=None):
    """Atualiza os detalhes de um livro existente."""
    mutation = """
    mutation ($id: Int!, $titulo: String, $descricao: String, $estado: String) {
        updateLivro(id: $id, titulo: $titulo, descricao: $descricao, estado: $estado) {
            livro {
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
        livro = resultado['data']['updateLivro']['livro']
        print(f"Livro atualizado: ID: {livro['id']}, Título: {livro['titulo']}")
    else:
        print("Erro ao atualizar o livro.")

def eliminar_livro(id_livro):
    """Elimina um livro do portfólio pelo ID."""
    mutation = """
    mutation ($id: Int!) {
        deleteLivro(id: $id) {
            ok
        }
    }
    """
    variables = {'id': id_livro}
    resultado = executar_query(mutation, variables)
    if resultado and 'data' in resultado:
        print(resultado['data']['deleteLivro']['ok'])
    else:
        print("Erro ao eliminar o livro.")