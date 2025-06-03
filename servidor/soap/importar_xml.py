import xml.etree.ElementTree as ET
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

def importar_xml(ficheiro='data/livros.xml'):
    tree = ET.parse(ficheiro)
    root = tree.getroot()
    for livro_el in root.findall("livro"):
        livro = {
            "id": int(livro_el.find("id").text),
            "titulo": livro_el.find("titulo").text,
            "descricao": livro_el.find("descricao").text,
            "estado": livro_el.find("estado").text,
        }
        if not collection.find_one({"id": livro["id"]}):
            collection.insert_one(livro)