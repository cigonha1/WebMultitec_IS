import sys
import os
import json
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

# Adiciona o diretório raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

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


# Modelo de Tarefa para o serviço SOAP
class TaskModel(ComplexModel):
    id = Integer
    titulo = Unicode
    descricao = Unicode
    estado = Unicode


# Classe do serviço SOAP
class TaskService(ServiceBase):

    @rpc(_returns=Array(TaskModel))
    def list_tasks(ctx):
        """Retorna todas as tarefas."""
        tasks = load_data()
        return tasks

    @rpc(Integer, _returns=TaskModel)
    def get_task(ctx, task_id):
        """Retorna uma tarefa específica pelo ID."""
        tasks = load_data()
        task = next((task for task in tasks if task["id"] == task_id), None)
        if task:
            return task
        raise ValueError("Task not found")

    @rpc(TaskModel, _returns=Unicode)
    def create_task(ctx, task):
        """Cria uma nova tarefa."""
        tasks = load_data()

        # Validar ID único
        if any(t["id"] == task.id for t in tasks):
            raise ValueError("Task with this ID already exists")

        tasks.append({"id": task.id, "titulo": task.titulo, "descricao": task.descricao, "estado": task.estado})
        save_data(tasks)
        return "Task created successfully"

    @rpc(Integer, TaskModel, _returns=Unicode)
    def update_task(ctx, task_id, task):
        """Atualiza uma tarefa existente."""
        tasks = load_data()
        existing_task = next((t for t in tasks if t["id"] == task_id), None)
        if not existing_task:
            raise ValueError("Task not found")

        # Atualizar a tarefa
        existing_task.update({"titulo": task.titulo, "descricao": task.descricao, "estado": task.estado})
        save_data(tasks)
        return "Task updated successfully"

    @rpc(Integer, _returns=Unicode)
    def delete_task(ctx, task_id):
        """Remove uma tarefa."""
        tasks = load_data()
        task = next((task for task in tasks if task["id"] == task_id), None)
        if not task:
            raise ValueError("Task not found")

        tasks.remove(task)
        save_data(tasks)
        return "Task deleted successfully"


# Configuração do servidor SOAP
application = Application(
    [TaskService],
    tns='soap.tasks',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 55555, wsgi_app)
    print("SOAP service is running on http://0.0.0.0:55555")
    server.serve_forever()