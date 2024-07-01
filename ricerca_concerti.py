import os
import time
from datetime import datetime
import pwinput
import geocoder

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
        global utente_attivo

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
        scelta = input("Inserisci un'opzione: \n1 - Logout\n2 - Ricerca\n3 - Mostra i tuoi biglietti\nq - Esci\n\nScelta: ")

        match scelta:
            case "1":
                logout()

            case "2":
                ricerca()

            case "3":
                mostra_biglietti()

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

@schermata
def mostra_biglietti():
    db_concerti.mostra_biglietti(utente_attivo)
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

    if db_concerti.check_credenziali(username, password):
        global utente_attivo
        utente_attivo = username

        print("Accesso riuscito.")
        input("Premi 'invio' per continuare...")
        return
    
    print("Nome utente o password non corretti.")
    input("Premi 'invio' per continuare...")
    return

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

    scelta = input("Come vuoi cercare il tuo concerto? \n1 - Cerca concerto\n2 - Cerca artista\n3 - Cerca date\n4 - Cerca per vicinanza\n5 - Cerca per genere\nq - Esci\n\nScelta: ")

    match scelta:
        case "1":
            ricerca_per_nome()
        case "2":
            ricerca_per_artista()
        case "3":
            ricerca_per_data()
        case "4": 
            ricerca_per_vicinanza()
        case "5":
            ricerca_per_genere()
        case "q":
            return
        case _:
            print("Operazione non valida. Riprova.")
            input("Premi 'invio' per continuare...")

@schermata
def ricerca_per_nome():

    """
    funzione che restituisce le info sul concerto cercato.
    """
    while True:
        nome_concerto = input("Inserisci il nome del concerto: ")
    
        concerto = db_concerti.ricerca_concerto({"nome":nome_concerto})

    # se non si trova alcun concerto con quel nome
        if not concerto:
            print("Non ho trovato alcun concerto con questo nome.")
            continua = input("Vuoi inserire un altro nome di concerto? [y/n]: ").strip().lower()
            if continua != "y":
                return
            else:
                continue

    # salvataggio id per potenziale acquisto
        id_concerto = concerto.get("_id")

        artisti = ', '.join([f"{artista.get("nome","Nome non disponibile")} {artista.get("cognome","Cognome non disponibile")}" for artista in concerto.get("artisti",[])])
        generi = ', '.join(concerto.get("generi",[]))
        data = concerto.get("data","Informazione non disponibile")
        città = concerto.get("città","Informazione non disponibile")
        provincia = concerto.get("provincia","Informazione non disponibile")
        location = concerto.get("location","Informazione non disponibile")
        indirizzo = concerto.get("indirizzo","Informazione non disponibile")

        info_concerto = f"""
        Alcune informazioni importanti sul tuo concerto:

--------------------------------------------------
    artisti: {artisti}
    generi: {generi}
    data: {data}
    città: {città}
    provincia: {provincia}
    location: {location}
    indirizzo: {indirizzo}
    """
        print(info_concerto)
        __acquista_biglietto(concerto)

@schermata
def __acquista_biglietto(concerto):

    print(f"Biglietti del concerto: {concerto.get("nome")}")

    biglietti = []

    # estrazione dei biglietti dal concerto
    for biglietto in concerto.get("biglietti",[]):
        tipo = biglietto.get("tipo","tipologia non disponibile")     
        prezzo = biglietto.get("prezzo","prezzo non disponibile")  
        disponibili = biglietto.get("numero_disponibili","Informazione non disponibile")
        biglietti.append(f"tipologia: {tipo}, prezzo: {prezzo} €, posti disponibili: {disponibili}")

    for i, biglietto in enumerate(biglietti, start=1):
        print(f"   {i}-    {biglietto}")

    print("\n--------------------------------------------------\n")

    scelta = input("Vuoi procedere all'acquisto di uno dei biglietti?\n[y/n]")
    
    while True:
        scelta = input("Vuoi procedere all'acquisto di uno dei biglietti?\n[y/n]: ").strip().lower()

        match scelta:
            case "y":
                try:
                    indice_biglietto = int(input("Inserisci l'indice del biglietto da acquistare (lascia vuoto per tornare al menu): ").strip())

                    if indice_biglietto == "":
                        return

                    if 1 <= indice_biglietto <= len(biglietti):
                        esito = db_concerti.acquisto_biglietto(concerto.get("_id"), indice_biglietto - 1, utente_attivo)

                        if esito:
                            print("Acquisto effettuato con successo!")
                        else:
                            print("Acquisto non riuscito. Riprova.")
                        input("Premi 'invio' per tornare al menu...")
                        return
                    else:
                        print("Indice del biglietto non valido. Riprova.")
                except ValueError:
                    print("Indice del biglietto non valido. Riprova.")
            case "n":
                print("Acquisto annullato.")
                input("Premi 'invio' per tornare al menu...")
                return
            case _:
                print("Scelta non valida. Riprova.")

@ schermata
def ricerca_per_artista():

    """
    funzione che restituisce la lista dei concerti in base al nome dell'artista cercato.
    funziona inserendo sia il nome completo, sia solo nome o solo cognome.
    eliminato case sensitive.
    """

    nome_artista = input("Inserisci il nome dell'artista che si esibirà: ")

    collection = db_concerti.db["concerti"]
    
    query = {}
    if " " in nome_artista:
        nome, cognome = nome_artista.split(" ", 1)
        query = {"artisti": {"$elemMatch":{"nome":{"$regex": nome, "$options":"i"}, "cognome":{"$regex": cognome, "$options":"i"}}}}
    else:
        query = {"artisti": {"$elemMatch": {"$or":[{"nome":{"$regex": nome_artista, "$options":"i"}}, {"cognome":{"$regex": nome_artista, "$options":"i"}}]}}}

    concerti = list(collection.find(query))

    numero_risultati = len(concerti)

    print("Questi sono i concerti disponibili:\n")
    for i, concerto in enumerate(concerti, start=1):
        print(f"{i}-   {concerto["nome"]}             [{concerto["data"]}]")
    
    while True:

        try:
            scelta = input("Inserisci l'indice del concerto a cui sei interessato (lascia vuoto per tornare al menu): ")

            if scelta == "":
                return
            
            scelta = int(scelta)

            if scelta > numero_risultati or scelta < 1:
                print("Scelta non valida. Riprova.")
                continue
            
            break

        except ValueError:
            print("Inserisci un numero.")

    __acquista_biglietto(concerti[scelta-1])
    
@schermata
def ricerca_per_data():

    """
    funzione che restituisce lista dei concerti tra due date.
    se le date non verranno inserite correttamente le richiede.
    se si desidera uscire premere 'invio'.
    Inserito anche il sort delle date.
    """

    while True:
        try:
            data1 = input("Inserisci la prima data (yyyy)-(mm)-(dd): ")
            if data1 == "":
                # NOTA: magari cambiare exit e mettere che torna al menu
                exit()
            datetime.strptime(data1,r"%Y-%m-%d")
            break
        except ValueError:
            print("Devi inserire la data correttamente")
        
    while True:
        try: 
            data2 = input("Inserisci la seconda data (yyyy)-(mm)-(dd): ")
            datetime.strptime(data1,r"%Y-%m-%d")
            break
        except ValueError:
            print("Devi inserire la data correttamente")
    
    date = [data1, data2]
    date.sort()
    
    collection = db_concerti.db["concerti"]

    query = {"data": {"$gte":date[0], "$lte":date[1]}}

    concerti = list(collection.find(query))

    numero_risultati = len(concerti)

    print("Questi sono i concerti disponibili:\n")
    for i, concerto in enumerate(concerti, start=1):
        print(f"{i}-   {concerto["nome"]}             [{concerto["data"]}]")
    
    while True:

        try:
            scelta = input("Inserisci l'indice del concerto a cui sei interessato (lascia vuoto per tornare al menu): ")

            if scelta == "":
                return
            
            scelta = int(scelta)

            if scelta > numero_risultati or scelta < 1:
                print("Scelta non valida. Riprova.")
                continue
            
            break

        except ValueError:
            print("Inserisci un numero.")

    __acquista_biglietto(concerti[scelta-1])

@schermata
def ricerca_per_vicinanza():
    
    """
    funzione che restituisce la lista dei concerti in base alla distanza da un punto di interesse.
    funziona con ip geolocation.
    """

    coordinate = geocoder.ip("me")

    lat, lon = coordinate.latlng
    
    print(f"Queste sono le tue coordinate: \nlatitudine: {lat}\nlongitudine: {lon}")

    while True:
        
        try:
            distanza_massima = input("Inserisci la distanza (in km) entro la quale vuoi visualizzare i concerti disponibili (lascia vuoto per tornare al menu): ")

            if distanza_massima == "":
                return

            distanza_massima = int(distanza_massima)
            
            break
        
        except ValueError:

            print("Non hai inserito un numero. Riprova")
            continue

    concerti = db_concerti.ricerca_per_vicinanza(lat, lon, distanza_massima)

    numero_risultati = len(concerti)

    if numero_risultati == 0:
        print("Non ci sono concerti entro il raggio scelto.")
        input("Premi 'invio' per continuare...")
        return

    for i, concerto in enumerate(concerti, start=1):
        print("----------------------------------------------------------------")
        print("      Concerto:", concerto.get("nome"))
        print("      Provincia:", concerto.get("provincia"))
        print(f"{i}     Città:", concerto.get("citta"))
        print("      Indirizzo:", concerto.get("indirizzo"))
        print("      Location:", concerto.get("location"))
        print("      Data:", concerto.get("data"))

    while True:

        try:
            scelta = input("Inserisci l'indice del concerto a cui sei interessato (lascia vuoto per tornare al menu): ")

            if scelta == "":
                return
            
            scelta = int(scelta)

            if scelta > numero_risultati or scelta < 1:
                print("Scelta non valida. Riprova.")
                continue
            
            break

        except ValueError:
            print("Inserisci un numero.")

    __acquista_biglietto(concerti[scelta-1])
    
@schermata
def ricerca_per_genere():

    genere = input("Inserisci il genere che preferisci: ")

    collection = db_concerti.db["concerti"]

    concerti = list(collection.find({"generi":genere}))
    
    numero_risultati = numero_risultati = len(concerti)

    print("\nEcco la lista dei concerti che potrebbero interessarti:\n\n------------------------------------------\n")
    for i, concerto in enumerate(concerti, start=1):
        print(f"{i} -  {concerto["nome"]}             [{concerto["data"]}]")
    
    

    while True:

        try:
            scelta = input("\nInserisci l'indice del concerto a cui sei interessato (lascia vuoto per tornare al menu): ")

            if scelta == "":
                return
            
            scelta = int(scelta)

            if scelta > numero_risultati or scelta < 1:
                print("\nScelta non valida. Riprova.")
                continue
            
            break

        except ValueError:
            print("\nInserisci un numero.")

    __acquista_biglietto(concerti[scelta-1])


if __name__ == "__main__":

    while True:
        menu()
