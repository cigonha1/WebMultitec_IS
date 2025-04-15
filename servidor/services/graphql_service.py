import os
import json
from flask import Flask, jsonify
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Int, List, Field, Schema, Mutation

# Caminho absoluto para o ficheiro de dados
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'tasks.json')


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


# Definir o modelo GraphQL para a Tarefa
class TaskType(ObjectType):
    id = Int()
    titulo = String()
    descricao = String()
    estado = String()


# Query para listar e obter tarefas
class Query(ObjectType):
    tasks = List(TaskType)
    task = Field(TaskType, id=Int(required=True))

    def resolve_tasks(root, info):
        """Resolver para listar todas as tarefas."""
        return load_data()

    def resolve_task(root, info, id):
        """Resolver para obter uma tarefa específica pelo ID."""
        tasks = load_data()
        return next((task for task in tasks if task["id"] == id), None)


# Mutation para criar, atualizar e eliminar tarefas
class CreateTask(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String(required=True)
        descricao = String(required=True)
        estado = String(required=True)

    task = Field(TaskType)

    def mutate(root, info, id, titulo, descricao, estado):
        tasks = load_data()

        # Verificar ID único
        if any(task["id"] == id for task in tasks):
            raise Exception("Task with this ID already exists")

        new_task = {"id": id, "titulo": titulo, "descricao": descricao, "estado": estado}
        tasks.append(new_task)
        save_data(tasks)
        return CreateTask(task=new_task)


class UpdateTask(Mutation):
    class Arguments:
        id = Int(required=True)
        titulo = String()
        descricao = String()
        estado = String()

    task = Field(TaskType)

    def mutate(root, info, id, titulo=None, descricao=None, estado=None):
        tasks = load_data()
        task = next((t for t in tasks if t["id"] == id), None)

        if not task:
            raise Exception("Task not found")

        # Atualizar os campos fornecidos
        if titulo is not None:
            task["titulo"] = titulo
        if descricao is not None:
            task["descricao"] = descricao
        if estado is not None:
            task["estado"] = estado

        save_data(tasks)
        return UpdateTask(task=task)


class DeleteTask(Mutation):
    class Arguments:
        id = Int(required=True)

    ok = String()

    def mutate(root, info, id):
        tasks = load_data()
        task = next((task for task in tasks if task["id"] == id), None)

        if not task:
            raise Exception("Task not found")

        tasks.remove(task)
        save_data(tasks)
        return DeleteTask(ok="Task deleted successfully")


# Definir as mutations no esquema
class Mutation(ObjectType):
    create_task = CreateTask.Field()
    update_task = UpdateTask.Field()
    delete_task = DeleteTask.Field()


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