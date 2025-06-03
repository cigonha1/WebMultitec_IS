import xml.etree.ElementTree as ET
from pymongo import MongoClient

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["biblioteca"]
collection = db["livros"]

def exportar_xml(ficheiro='data/livros.xml'):
    livros = list(collection.find({}, {"_id": 0}))
    root = ET.Element("livros")
    for livro in livros:
        livro_el = ET.SubElement(root, "livro")
        for chave, valor in livro.items():
            campo = ET.SubElement(livro_el, chave)
            campo.text = str(valor)
    arvore = ET.ElementTree(root)
    arvore.write(ficheiro, encoding='utf-8', xml_declaration=True)