import json
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

def importar_json(ficheiro='data/livros.json'):
    with open(ficheiro, 'r', encoding='utf-8') as f:
        livros = json.load(f)
    for livro in livros:
        if not collection.find_one({"id": livro["id"]}):
            collection.insert_one(livro)