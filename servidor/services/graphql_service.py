import os
import json
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, List, Field, Schema, Mutation

# Caminho absoluto para o ficheiro de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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


# Mutation para criar, atualizar e eliminar livros
class CreateLivro(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String(required=True)
        descricao = String(required=True)
        estado = String(required=True)

    livro = Field(LivroType)

    def mutate(root, info, id, titulo, descricao, estado):
        livros = load_data()

        # Verificar ID único
        if any(livro["id"] == id for livro in livros):
            raise Exception("Livro with this ID already exists")

        new_livro = {"id": id, "titulo": titulo, "descricao": descricao, "estado": estado}
        livros.append(new_livro)
        save_data(livros)
        return CreateLivro(livro=new_livro)


class UpdateLivro(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String()
        descricao = String()
        estado = String()

    livro = Field(LivroType)

    def mutate(root, info, id, titulo=None, descricao=None, estado=None):
        livros = load_data()
        livro = next((l for l in livros if l["id"] == id), None)

        if not livro:
            raise Exception("Livro not found")

        # Atualizar os campos fornecidos
        if titulo is not None:
            livro["titulo"] = titulo
        if descricao is not None:
            livro["descricao"] = descricao
        if estado is not None:
            livro["estado"] = estado

        save_data(livros)
        return UpdateLivro(livro=livro)


class DeleteLivro(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = String()

    def mutate(root, info, id):
        livros = load_data()
        livro = next((livro for livro in livros if livro["id"] == id), None)

        if not livro:
            raise Exception("Livro not found")

        livros.remove(livro)
        save_data(livros)
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