import os
import time
from datetime import datetime
import pwinput

# importazione funzioni db
import db

# creazione oggetto db
db_concerti = db.DatabaseConcerti()

# variabile che determina l'utente attivo
utente_attivo = None

# wrapper delle funzioni schermata
def schermata(f):
    def wrapper(*args, **kwargs):
        """Questa funzione pulisce il terminale e stampa delle informazioni:
        - utente attivo
        """

        # importazione variabile globale
        global utente_attivoù

        if os.name == 'nt':
            # Per Windows
            os.system('cls')
        else:
            # Per Unix/Linux/macOS
            os.system('clear')

        print("Utente attivo: ", end="")

        if utente_attivo:
            print(utente_attivo)
        else:
            print("guest")

        print("\n")
        
        return f(*args, **kwargs)
    
    return wrapper

@schermata
def menu():
    global utente_attivo

    # menu se l'utente è loggato
    if utente_attivo:
        scelta = input("Inserisci un'opzione: \n1 - Logout\n2 - Ricerca\nq - Esci\n\nScelta: ")

        match scelta:
            case "1":
                logout()

            case "2":
                ricerca()

            case "q":
                print("Sto eseguendo l'uscita dal programma...")
                time.sleep(1)
                exit(0)

            case _:
                print("Scelta non valida. Riprova.")
                input("Premi 'invio' per continuare...")


    # menu se l'utente non è già loggato
    else:
        scelta = input("Inserisci un'opzione: \n1 - Login\n2 - Registrazione\nq - Esci\n\nScelta: ")
        
        match scelta:
            case "1":
                login()

            case "2":
                registrazione()

            case "q":
                print("Sto eseguendo l'uscita dal programma...")
                time.sleep(1)
                exit(0)

            case _:
                print("Scelta non valida. Riprova.")
                input("Premi 'invio' per continuare...")

@ schermata
def registrazione():

    print("Questa è la procedura di registrazione di un nuovo utente.\nSe vuoi uscire in qualsiasi momento lascia il campo vuoto.")

    # inserimento username
    while True:
        username = input("Inserisci il nome utente: ")

        if username == "":
            return
        
        if len(username) < 5:
            print("Il nome utente deve essere lungo almeno 5 caratteri.")
            continue

        ### 
        ### TODO: aggiungere check sul db esistenza del nome utente. Se già esiste, fare reinserire
        ###

        if db_concerti.esistenza_utente(username) == True:
            print("Nome utente già esistente. Riprova.")
            continue
        
        break
    
    # inserimento nome e cognome
    nome = input("Inserisci il tuo nome: ")

    if nome == "":
        return

    cognome = input("Inserisci il tuo cognome: ")

    if cognome == "":
        return

    # inserimento data di nascita
    while True:

        try:
            anno = input("Inserisci il tuo anno di nascita (yyyy): ")

            if anno == "":
                return
            
            anno = int(anno)

            mese = input("Inserisci il tuo mese di nascita (mm): ")
            
            if mese == "":
                return
            
            mese = int(mese)

            giorno = input("Inserisci il tuo giorno di nascita (dd): ")

            if giorno == "":
                return
            
            giorno = int(giorno)


            # conversione a datetime
            data_nascita = datetime(
                anno,
                mese,
                giorno
            )
            
            # chance di verifica della correttezza della data 
            verifica = input(f"La data di nascita è corretta?\n{data_nascita.strftime("%d/%m/%Y")} [y/n]")

            if verifica == "":
                return

            if verifica != "y":
                print("Inserimento data di nascita annullato. Riprova.")
                continue

            # se tutto a posto, esci
            break

        except Exception:
            print("Data non valida. Riprova.")
            continue

    # inserimento password
    while True:
        password = pwinput.pwinput(prompt='Inserisci la password: ', mask='*')

        if password == "":
            return
        
        if len(password) < 8:
            print("La password deve essere lunga almeno 8 caratteri.")
            continue
        
        break

    info_nuovo_utente = {
        "username": username,
        "nome": nome,
        "cognome": cognome,
        "data_nascita": data_nascita,
        "password": password
    }

    db_concerti.inserisci_nuovo_utente(info_nuovo_utente)

    print("Utente creato con successo!")
    input("Premi 'invio' per continuare...")

@schermata
def login():

    print("Questa è la procedura di login.")

    # inserimento username
    username = input("Inserisci il nome utente: ")

    password = pwinput.pwinput(prompt='Inserisci la password: ', mask='*')

    ###
    ### TODO: ricerca della coppia usename e password nel db per effettuare il login
    ###

    # se il login ha successo, cambia l'utente attivo TODO: da cambiare l'if
    if True:
        global utente_attivo
        utente_attivo = username

        print("Accesso riuscito.")
        input("Premi 'invio' per continuare...")


@schermata
def logout():

    scelta = input("Sei sicuro di voler eseguire il logout? [y/n]")

    match scelta:
        case "y":
            global utente_attivo
            utente_attivo = None
            print("Logout eseguito con successo.")

        case "n":
            print("Logout annullato.")

        case _:
            print("Scelta non valida. Riprova.")
        
    input("Premi 'invio' per continuare...")

@schermata
def ricerca():

    scelta = input("Inserisci un'opzione: \n1 - Cerca concerto\n2 - Cerca artista\n3 - Cerca date\n4 - Cerca luogo\n5 - Consigliami un concerto\nq - Esci\n\nScelta: ")

    match scelta:
        case "1":
            ricerca_per_concerto()
           # acquista_biglietto(id_concerto)
        case "2":
            ricerca_per_artista()
           # acquista_biglietto()
        case "3":
            print("Inserisci le date:")
           # ricerca_per_data()
           # acquista_biglietto()
        case "4": 
            print("Inserisci località:")
           # ricerca_per_luogo()
           # acquista_biglietto()
        case "5":
            print("Ecco alcuni concerti che potrebbero interessarti:")
           # concerti_consigliati()
           # acquista_biglietto
        case "q":
            print("Sto tornando al menù...")
            time.sleep(1)
            exit(0)
        case _:
            print("Operazione non valida. Riprova.")
            input("Premi 'invio' per continuare...")

@schermata
def ricerca_per_concerto():

    nome_concerto = input("Inserisci il nome del concerto: ")
    
    collection = db.db["concerti"]
    concerto = collection.find_one({"nome":nome_concerto})

    if concerto:
        # id_concerto = concerto.get("_id")
        artisti = ', '.join([f"{artista.get("nome","Nome non disponibile")} {artista.get("cognome","Cognome non disponibile")}" for artista in concerto.get("artisti",[])])
        generi = ', '.join(concerto.get("generi",[]))
        data = concerto.get("data","Informazione non disponibile")
        città = concerto.get("città","Informazione non disponibile")
        provincia = concerto.get("provincia","Informazione non disponibile")
        location = concerto.get("location","Informazione non disponibile")
        indirizzo = concerto.get("indirizzo","Informazione non disponibile")
        biglietti = [] 
        for biglietto in concerto.get("biglietti",[]):
            tipo = biglietto.get("tipo","tipologia non disponibile")     
            prezzo = biglietto.get("prezzo","prezzo non disponibile")  
            disponibili = biglietto.get("numero_disponibili","Informazione non disponibile")
            biglietti.append(f"tipologia: {tipo}, prezzo: {prezzo} €, posti disponibili: {disponibili}")

        print("Alcune informazioni importanti sul tuo concerto:\n")
        print(f"artisti: {artisti}\ngeneri: {generi}\ndata: {data}\ncittà: {città}\nprovincia: {provincia}\nlocation: {location}\nindirizzo: {indirizzo}\nbiglietti:")
        for biglietto in biglietti:
            print(f"       {biglietto}")
        
        input("Premi 'invio' per continuare...")
    else:
        print("Non trovato alcun concerto con questo nome")
        input("Premi 'invio' per continuare...")

@ schermata
def ricerca_per_artista():

    nome_artista = input("Inserisci il nome dell'artista che si esibirà: ")

    collection = db.db["concerti"]
    
    query = {}
    if " " in nome_artista:
        nome, cognome = nome_artista.split(" ", 1)
        query = {"artisti": {"$elemMatch":{"nome":{"$regex": nome, "$options":"i"}, "cognome":{"$regex": cognome, "$options":"i"}}}}
    else:
        query = {"artisti": {"$elemMatch": {"$or":[{"nome":{"$regex": nome_artista, "$options":"i"}}, {"cognome":{"$regex": nome_artista, "$options":"i"}}]}}}

    nomi_concerti = collection.find(query)
    for concerto in nomi_concerti:
        print(concerto["nome"])
    
    input("Premi 'invio' per continuare...")
  


if __name__ == "__main__":
    while True:
        menu()



