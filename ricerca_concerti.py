import os
import time
from datetime import datetime
import pwinput

# importazione funzioni db
import db

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
        scelta = input("Inserisci un'opzione: \n1 - Logout\n2 - Ricerca\nq - Esci\n\nScelta: ")

        match scelta:
            case "1":
                logout()

            case "2":
                # ricerca()
                # TODO
                pass

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

    db.inserisci_nuovo_utente(info_nuovo_utente)

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


if __name__ == "__main__":
    while True:
        menu()