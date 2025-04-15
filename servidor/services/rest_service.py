import sys
import os
import json
from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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

# Classe para o gerenciamento de tarefas
class Task(Resource):
    def get(self, task_id=None):
        tasks = load_data()
        if task_id is None:
            return jsonify(tasks)
        task = next((task for task in tasks if task["id"] == task_id), None)
        if task:
            return jsonify(task)
        return {"message": "Task not found"}, 404

    def post(self):
        data = request.get_json()
        tasks = load_data()

        # Validar ID único
        if any(task["id"] == data["id"] for task in tasks):
            return {"message": "Task with this ID already exists"}, 400

        tasks.append(data)
        save_data(tasks)
        return {"message": "Task created successfully"}, 201

    def put(self, task_id):
        data = request.get_json()
        tasks = load_data()
        task = next((task for task in tasks if task["id"] == task_id), None)
        if not task:
            return {"message": "Task not found"}, 404

        # Atualizar a tarefa
        task.update(data)
        save_data(tasks)
        return {"message": "Task updated successfully"}

    def delete(self, task_id):
        tasks = load_data()
        task = next((task for task in tasks if task["id"] == task_id), None)
        if not task:
            return {"message": "Task not found"}, 404

        tasks.remove(task)
        save_data(tasks)
        return {"message": "Task deleted successfully"}

# Rotas da API
api.add_resource(Task, '/tasks', '/tasks/<int:task_id>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55556, debug=True)