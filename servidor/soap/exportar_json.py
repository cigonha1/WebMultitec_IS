import json
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

def exportar_json(ficheiro='data/livros.json'):
    livros = list(collection.find({}, {"_id": 0}))
    with open(ficheiro, 'w', encoding='utf-8') as f:
        json.dump(livros, f, indent=4, ensure_ascii=False)