import requests

BASE_URL = "http://rest.Dmgp.local/"  # URL do serviço REST 

# === CREATE ===
def create_book():
    payload = {
        "id": 1,  # Certifica-te de que o ID é único
        "titulo": "Livro Exemplo",
        "descricao": "Este é um livro de teste para o portefólio.",
        "estado": "pendente"  # Pode ser "pendente" ou "concluído"
    }
    response = requests.post(f"{BASE_URL}/tasks", json=payload)
    print("✅ Livro Criado:", response.json())

# === READ ALL ===
def get_all_books():
    response = requests.get(f"{BASE_URL}/tasks")
    if response.status_code == 200:
        print("📋 Livros:")
        for book in response.json():
            print(f"- ID: {book['id']}, Título: {book['titulo']}, Estado: {book['estado']}")
    else:
        print(f"Erro ao obter lista de livros: {response.status_code}")

# === READ BY ID ===
def get_book_by_id(book_id):
    response = requests.get(f"{BASE_URL}/tasks/{book_id}")
    if response.status_code == 200:
        print(f"🔎 Livro ID {book_id}:", response.json())
    else:
        print(f"Erro ao obter livro ID {book_id}: {response.status_code}")

# === UPDATE ===
def update_book(book_id):
    payload = {
        "titulo": "Livro Atualizado",
        "descricao": "Descrição atualizada para o livro.",
        "estado": "concluído"  # Alternar estado para "concluído"
    }
    response = requests.put(f"{BASE_URL}/tasks/{book_id}", json=payload)
    if response.status_code == 200:
        print("✏️ Livro Atualizado:", response.json())
    else:
        print(f"Erro ao atualizar livro ID {book_id}: {response.status_code}")

# === DELETE ===
def delete_book(book_id):
    response = requests.delete(f"{BASE_URL}/tasks/{book_id}")
    if response.status_code == 200:
        print("🗑️ Livro Apagado:", response.json())
    else:
        print(f"Erro ao apagar livro ID {book_id}: {response.status_code}")

# === FLUXO COMPLETO ===
if __name__ == "__main__":
    print("🔨 Criar livro...")
    create_book()

    print("\n📋 Ler todos os livros...")
    get_all_books()

    print("\n🔎 Ler livro por ID 1...")
    get_book_by_id(1)

    print("\n✏️ Atualizar livro ID 1...")
    update_book(1)

    print("\n🗑️ Apagar livro ID 1...")
    delete_book(1)

    print("\n📋 Ler todos os livros depois das alterações...")
    get_all_books()