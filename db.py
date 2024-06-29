from pymongo import MongoClient

# definizione costanti
uri = "mongodb://localhost:27017"
nome_db = "db_concerti"

# connessione al database MongoDB
client = MongoClient(uri)
db = client[nome_db]

def inserisci_nuovo_utente(utente: dict):
    """
    Funzione che inserisce un utente nel database
    """

    global client, db

    # selezione della collezione
    coll = db["users"]

    coll.insert_one(utente)