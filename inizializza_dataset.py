import json
from pymongo import MongoClient

import os
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

# definizione costanti
client = None
nome_db = "db_concerti"

def connessione_db(uri: str):
    """
    Funzione che inizializza la connessione con il db
    """

    global client

    client = MongoClient(uri)


def estrai_concerti() -> tuple:
    """
    Funzione che estrare in concerti dal file json e li inserisce nel db
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
    connessione_db(uri="mongodb+srv://giulioghislandi:NsR0y8Sf1ypk11O8@cluster0.nlkhmot.mongodb.net/")

    # estrazione concerti
    concerti = estrai_concerti()
    
    # inserimento concerti
    insert(concerti, "concerti")

    # chiusura connessione
    client.close()

