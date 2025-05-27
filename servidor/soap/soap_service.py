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


# Modelo de Livro para o serviço SOAP
class LivroModel(ComplexModel):
    id = Integer
    titulo = Unicode
    descricao = Unicode
    estado = Unicode


# Classe do serviço SOAP
class LivroService(ServiceBase):

    @rpc(_returns=Array(LivroModel))
    def list_livros(ctx):
        """Retorna todos os livros."""
        livros = load_data()
        return livros

    @rpc(Integer, _returns=LivroModel)
    def get_livro(ctx, livro_id):
        """Retorna um livro específico pelo ID."""
        livros = load_data()
        livro = next((livro for livro in livros if livro["id"] == livro_id), None)
        if livro:
            return livro
        raise ValueError("Livro not found")

    @rpc(LivroModel, _returns=Unicode)
    def create_livro(ctx, livro):
        """Cria um novo livro."""
        livros = load_data()

        # Validar ID único
        if any(l["id"] == livro.id for l in livros):
            raise ValueError("Livro with this ID already exists")

        livros.append({"id": livro.id, "titulo": livro.titulo, "descricao": livro.descricao, "estado": livro.estado})
        save_data(livros)
        return "Livro created successfully"

    @rpc(Integer, LivroModel, _returns=Unicode)
    def update_livro(ctx, livro_id, livro):
        """Atualiza um livro existente."""
        livros = load_data()
        existing_livro = next((l for l in livros if l["id"] == livro_id), None)
        if not existing_livro:
            raise ValueError("Livro not found")

        # Atualizar o livro
        existing_livro.update({"titulo": livro.titulo, "descricao": livro.descricao, "estado": livro.estado})
        save_data(livros)
        return "Livro updated successfully"

    @rpc(Integer, _returns=Unicode)
    def delete_livro(ctx, livro_id):
        """Remove um livro."""
        livros = load_data()
        livro = next((livro for livro in livros if livro["id"] == livro_id), None)
        if not livro:
            raise ValueError("Livro not found")

        livros.remove(livro)
        save_data(livros)
        return "Livro deleted successfully"


# Configuração do servidor SOAP
application = Application(
    [LivroService],
    tns='soap.livros',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 55555, wsgi_app)
    print("SOAP service is running on http://0.0.0.0:55555")
    server.serve_forever()