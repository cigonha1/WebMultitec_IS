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

# Classe para o gerenciamento de livros
class Livro(Resource):
    def get(self, livro_id=None):
        livros = load_data()
        if livro_id is None:
            return jsonify(livros)
        livro = next((livro for livro in livros if livro["id"] == livro_id), None)
        if livro:
            return jsonify(livro)
        return {"message": "Livro not found"}, 404

    def post(self):
        data = request.get_json()
        livros = load_data()

        # Validar ID único
        if any(livro["id"] == data["id"] for livro in livros):
            return {"message": "Livro with this ID already exists"}, 400

        livros.append(data)
        save_data(livros)
        return {"message": "Livro created successfully"}, 201

    def put(self, livro_id):
        data = request.get_json()
        livros = load_data()
        livro = next((livro for livro in livros if livro["id"] == livro_id), None)
        if not livro:
            return {"message": "Livro not found"}, 404

        # Atualizar o livro
        livro.update(data)
        save_data(livros)
        return {"message": "Livro updated successfully"}

    def delete(self, livro_id):
        livros = load_data()
        livro = next((livro for livro in livros if livro["id"] == livro_id), None)
        if not livro:
            return {"message": "Livro not found"}, 404

        livros.remove(livro)
        save_data(livros)
        return {"message": "Livro deleted successfully"}

# Rotas da API
api.add_resource(Livro, '/livros', '/livros/<int:livro_id>')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=55556, debug=True)