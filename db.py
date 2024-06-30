from pymongo import MongoClient


class DatabaseConcerti:

    def __init__(self) -> None:
        # definizione costanti
        self.uri = "mongodb://localhost:27017"
        self.nome_db = "db_concerti"

        # connessione al database MongoDB
        self.client = MongoClient(self.uri)
        self.db = self.client[self.nome_db]

    def inserisci_nuovo_utente(self, utente: dict):
        """
        Funzione che inserisce un utente nel database
        """
        # selezione della collezione
        coll = self.db["users"]

        coll.insert_one(utente)

    def esistenza_utente(self, username):

        # selezione della collezione
        coll = self.db["users"]

        # query di ricerca dell'utente
        user = coll.find_one({"username": username})

        if user:
            return True
        
        return False
    
    def check_credenziali(self, username, password):
        # selezione della collezione
        coll = self.db["users"]

        # query di ricerca dell'utente
        user = coll.find_one({"username": username, "password": password})

        if user:
            return True
        
        return False