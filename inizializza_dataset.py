import json
from pymongo import MongoClient

# importazione delle costanti del db
from db import uri
from db import nome_db

# impostazione della cartella di esecuzione corretta
import os
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)


def connessione_db(uri: str):
    """
    Funzione che inizializza la connessione con il db
    """

    global client

    client = MongoClient(uri)


def estrai_concerti() -> tuple:
    """
    Funzione che estrare i concerti dal file json e li inserisce nel db
    """

    with open("data/concerti.json", "r") as file_concerti:
        concerti = json.load(file_concerti)

    return concerti


def insert(data, nome_collezione):
    """
    Funzione che inserisce lista di oggetti json nel db
    """

    db = client[nome_db]
    coll = db[nome_collezione]

    coll.insert_many(data)


if __name__ == '__main__':
    connessione_db(uri)

    # estrazione concerti
    concerti = estrai_concerti()
    
    # inserimento concerti
    insert(concerti, "concerti")

    # chiusura connessione
    client.close()

