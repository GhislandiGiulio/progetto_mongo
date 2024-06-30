from pymongo import MongoClient
import geocoder

class DatabaseConcerti:

    def __init__(self) -> None:
        # definizione costanti
        self.uri = "mongodb+srv://emanuelesassi:nsiZ2wXT69aa1kx5@cluster0.3xxugqa.mongodb.net/"
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
    
    def __id_utente(self, username):

        coll = self.db["users"]

        # query di ricerca dell'utente
        user = coll.find_one({"username": username})

        return user["_id"]
    
    def check_credenziali(self, username, password):
        # selezione della collezione
        coll = self.db["users"]

        # query di ricerca dell'utente
        user = coll.find_one({"username": username, "password": password})

        if user:
            return True
        
        return False
    
    def ricerca_concerto(self, concerto: dict):

        coll = self.db["concerti"]

        results = coll.find_one(concerto)

        return results
    
    def acquisto_biglietto(self, id_concerto, indice_biglietto, utente):
        
        coll = self.db["concerti"]


        # ricerca del concerto
        concerto = coll.find_one(
                {"_id": id_concerto}
        )

        # controllo se il tipo di biglietto è disponibile
        biglietto = concerto["biglietti"][indice_biglietto]

        if biglietto["numero_disponibili"] <= 0:
            return False
        
        # diminuzione del numero di biglietti disponibili
        coll.find_one_and_update(
                {"_id": id_concerto, "biglietti.{}".format(indice_biglietto): {"$exists": True}},
                {"$inc": {"biglietti.{}.numero_disponibili".format(indice_biglietto): -1}},
                return_document=True
            )
        
        # aggiunta del biglietto nel db

        coll = self.db["biglietti"]

        coll.insert_one({"id_concerto": id_concerto, "id_utente": self.__id_utente(utente), "tipologia": biglietto["tipo"], "prezzo": biglietto["prezzo"]})

        return True
    
    def mostra_biglietti(self, utente):
        
        coll = self.db["biglietti"]

        id_utente = self.__id_utente(utente)

        query = {"id_utente": id_utente}
        
        biglietti = list(coll.find(query))

        if len(biglietti) == 0:
            print("Non hai biglietti")
        
        for biglietto in biglietti:
            
            coll = self.db["concerti"]  

            id_concerto = biglietto["id_concerto"]

            query = {"_id": id_concerto}

            concerto = coll.find_one(query)

            print("----------------------------------------------------------------")
            print("Concerto:", concerto.get("nome"))
            print("Provincia:", concerto.get("provincia"))
            print("Città:", concerto.get("citta"))
            print("Indirizzo:", concerto.get("indirizzo"))
            print("Location:", concerto.get("location"))
            print("Data:", concerto.get("data"))

    def crea_indice_geospaziale(self):
        coll = self.db["concerti"]

        coll.create_index([("coordinate", "2dsphere")])
        
        # le mie coordinate
        coordinate = geocoder.ip("me")

        print(coordinate.latlng)

    

if __name__ == "__main__":

    pass