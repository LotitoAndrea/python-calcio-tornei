# SGTC — Sistema di Gestione Tornei di Calcio Scolastici

Backend REST costruito con **FastAPI** e **Python** puro.  
Nessun database, nessun ORM: tutti i dati sono conservati in dizionari in memoria.

---

## Struttura progetto

```
python-calcio/
├── app/
│   ├── __init__.py     # package marker
│   ├── main.py         # route FastAPI
│   ├── services.py     # logica di business
│   └── store.py        # dati in memoria (dizionari)
├── requirements.txt
└── README.md
```

---

## Requisiti

- Python 3.10+
- pip

---

## Installazione e avvio

```bash
# 1. Clona il repository
git clone <url-repo>
cd python-calcio

# 2. Crea e attiva il virtualenv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Installa le dipendenze
pip install -r requirements.txt

# 4. Avvia il server
uvicorn app.main:app --reload
```

Il server sarà disponibile su: **http://127.0.0.1:8000**

Documentazione interattiva (Swagger UI): **http://127.0.0.1:8000/docs**

---

## Endpoint API

### Tornei

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei` | Crea un torneo |
| `GET` | `/api/v1/tornei` | Lista tutti i tornei |
| `GET` | `/api/v1/tornei/{id}` | Dettaglio torneo |
| `PATCH` | `/api/v1/tornei/{id}` | Aggiorna torneo |
| `DELETE` | `/api/v1/tornei/{id}` | Elimina torneo |

### Squadre

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/squadre` | Aggiunge una squadra |
| `GET` | `/api/v1/tornei/{torneoId}/squadre` | Lista squadre del torneo |

### Giocatori

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/squadre/{squadraId}/giocatori` | Aggiunge un giocatore |
| `DELETE` | `/api/v1/squadre/{squadraId}/giocatori/{giocatoreId}` | Rimuove un giocatore |

### Gironi

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/gironi/genera` | Genera i gironi |
| `GET` | `/api/v1/tornei/{torneoId}/gironi` | Lista gironi del torneo |

### Partite

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/partite/genera-calendario` | Genera il calendario |
| `GET` | `/api/v1/tornei/{torneoId}/partite` | Lista partite del torneo |
| `POST` | `/api/v1/partite/{partitaId}/risultato` | Inserisce/aggiorna risultato |

### Classifica

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `GET` | `/api/v1/gironi/{gironeId}/classifica` | Classifica del girone |

---

## Esempio d'uso (flusso completo)

```bash
BASE="http://127.0.0.1:8000/api/v1"

# 1. Crea un torneo
curl -X POST $BASE/tornei \
  -H "Content-Type: application/json" \
  -d '{"nome": "Torneo Primavera", "anno": 2025}'

# 2. Aggiungi squadre (usa l'ID del torneo restituito, es. "abc12345")
curl -X POST $BASE/tornei/abc12345/squadre \
  -H "Content-Type: application/json" \
  -d '{"nome": "Aquile FC"}'

# 3. Aggiungi giocatori (usa l'ID squadra restituito, es. "def67890")
curl -X POST $BASE/squadre/def67890/giocatori \
  -H "Content-Type: application/json" \
  -d '{"nome": "Mario", "cognome": "Rossi", "numero_maglia": 10}'

# 4. Genera i gironi
curl -X POST $BASE/tornei/abc12345/gironi/genera \
  -H "Content-Type: application/json" \
  -d '{"num_gironi": 2}'

# 5. Genera il calendario
curl -X POST $BASE/tornei/abc12345/partite/genera-calendario

# 6. Inserisci un risultato (usa l'ID partita, es. "ghi11111")
curl -X POST $BASE/partite/ghi11111/risultato \
  -H "Content-Type: application/json" \
  -d '{"gol_casa": 3, "gol_ospite": 1}'

# 7. Leggi la classifica (usa l'ID girone, es. "jkl22222")
curl $BASE/gironi/jkl22222/classifica
```

---

## Note tecniche

- I dati **non sono persistenti**: al riavvio del server vengono azzerati.
- Il sistema di punti segue il regolamento standard: **vittoria = 3 pt**, **pareggio = 1 pt**, **sconfitta = 0 pt**.
- La classifica è ordinata per: punti → differenza reti → gol fatti.
- È possibile correggere un risultato già inserito: la classifica viene aggiornata automaticamente.
