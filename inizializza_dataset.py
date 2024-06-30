import json
from pymongo import MongoClient

import db

# impostazione della cartella di esecuzione corretta
import os
script_dir = os.path.dirname(__file__)
os.chdir(script_dir)

# inizializzazione della connessione
db_concerti = db.DatabaseConcerti() 

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

    coll = db_concerti.db["concerti"]

    coll.insert_many(data)


if __name__ == '__main__':

    # estrazione concerti
    concerti = estrai_concerti()
    
    # inserimento concerti
    insert(concerti, "concerti")

    # chiusura connessione
    db_concerti.client.close()

