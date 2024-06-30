# Progetto MongoDB - Gruppo 7
## Descrizione
Il progetto consiste nella creazione di un database di concerti e un interfaccia CLI che consenta di:
- Visualizzare artista/i che partecipa/no al concerto
- Risalire al nome del concerto
- Ricerca di concerti in un intervallo di date
- Ricerca per vicinanza (concerto entro tot km da un punto)

## 1. Clonazione della repo 
Crea una cartella apposita per il tuo progetto. Il nome non ha importanza.

Apri una shell nella cartella in cui vuoi eseguire il progetto ed esegui i seguenti comandi:
``` powershell
git clone https://github.com/GhislandiGiulio/progetto_mongo.git .
``` 


## 2. Download python 3.12
Se non è già installato, scarica Python 3.12. Se è già installato, assicurati che sia la versione attiva nel sistema di python.
### Windows:
```powershell
winget install -e --id Python.Python.3.12
```

### macOS (homebrew)
```powershell
brew install python@3.12
```

## 3. Creazione virtual environment

### Windows
```powershell
py -3.12 -m venv .venv
``` 

### macOS
``` powershell
python3.12 -m venv .venv
``` 

## 4. Attivazione virtual environment
### Windows Powershell
``` powershell
[PATH_DIRECTORY_PROGETTO]\.venv\Scripts\Activate.ps1
``` 
### macOS
``` powershell
source [PATH_DIRECTORY_PROGETTO]/.venv/bin/activate
``` 


## 5. Installazione delle dipendenze
Installazione moduli richiesti per eseguire lo script python:
``` powershell
pip install -r requirements.txt
```

## 6. Installazione di MongoDB server con Docker
Se non già installato, scarica l'eseguibile di Docker dal [sito ufficiale](https://www.docker.com/products/docker-desktop/).
Una volta installato, fai il pull dell'imagine di Mongo:
``` powershell
docker pull mongo 
```
Adesso crea un container con port-forwarding:
``` powershell
docker run -d --name my_mongo -p 27017:27017 mongo
```

## 7. Inizializzazione del db
Se hai accesso al db, puoi eseguire lo script "inizializza_dataset.py" per inizializzare il db con 33 concerti con cui testare lo script principale.