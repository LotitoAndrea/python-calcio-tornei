# SGTC — Sistema di Gestione Tornei di Calcio Scolastici

Applicazione **full-stack** per la creazione e gestione di tornei di calcio scolastici.

- **Backend**: REST API costruita con **FastAPI** e **Python 3.10+**, persistenza tramite **TinyDB** (file `database.json`).
- **Frontend**: Interfaccia web multi-pagina in **HTML + Bootstrap 5 + JavaScript vanilla**, servita direttamente dal backend come file statici.

---

## Struttura del progetto

```
python-calcio/
├── backend/
│   ├── __init__.py     # package marker
│   ├── main.py         # route FastAPI + CORS + servizio static files
│   ├── services.py     # logica di business
│   └── store.py        # store in memoria (dizionari)
├── frontend/
│   ├── index.html      # Homepage — lista e creazione tornei
│   ├── torneo.html     # Dettaglio torneo (squadre, gironi, partite, classifica)
│   ├── squadra.html    # Dettaglio squadra (rosa giocatori)
│   ├── css/
│   │   └── style.css   # Tema calcistico custom
│   └── js/
│       ├── api.js      # Modulo centralizzato per le chiamate REST
│       ├── utils.js    # Funzioni condivise (toast, badge, query string)
│       ├── tornei.js   # Logica index.html
│       ├── torneo.js   # Logica torneo.html
│       └── squadra.js  # Logica squadra.html
├── database.json       # Database TinyDB (persistente)
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
uvicorn backend.main:app --reload
```

Un solo comando avvia sia il backend che il frontend.

| Risorsa | URL |
|---------|-----|
| **Applicazione web** | http://127.0.0.1:8000/ |
| **Swagger UI** (API docs) | http://127.0.0.1:8000/docs |
| **ReDoc** | http://127.0.0.1:8000/redoc |

---

## Flusso d'uso (interfaccia web)

1. Apri **http://127.0.0.1:8000/** nel browser
2. **Crea un torneo** inserendo nome e anno
3. Apri il torneo e **aggiungi almeno 2 squadre**
4. Clicca su una squadra per aggiungere **giocatori** alla rosa
5. Torna al torneo → **Genera Gironi** scegliendo il numero di gironi
6. **Genera Calendario** per creare le partite round-robin nei gironi
7. **Inserisci i risultati** direttamente su ogni partita (modificabili in seguito)
8. Seleziona un girone dal menu per visualizzare la **classifica aggiornata in tempo reale**

---

## Endpoint API

### Tornei

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei` | Crea un torneo |
| `GET` | `/api/v1/tornei` | Lista tutti i tornei |
| `GET` | `/api/v1/tornei/{id}` | Dettaglio torneo |
| `PATCH` | `/api/v1/tornei/{id}` | Aggiorna torneo (nome, anno, stato) |
| `DELETE` | `/api/v1/tornei/{id}` | Elimina torneo |

### Squadre

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/squadre` | Aggiunge una squadra al torneo |
| `GET` | `/api/v1/tornei/{torneoId}/squadre` | Lista squadre del torneo |

### Giocatori

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `GET` | `/api/v1/squadre/{squadraId}/giocatori` | Lista giocatori della squadra |
| `POST` | `/api/v1/squadre/{squadraId}/giocatori` | Aggiunge un giocatore |
| `DELETE` | `/api/v1/squadre/{squadraId}/giocatori/{giocatoreId}` | Rimuove un giocatore |

### Gironi

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/gironi/genera` | Genera i gironi (distribuisce le squadre) |
| `GET` | `/api/v1/tornei/{torneoId}/gironi` | Lista gironi del torneo |

### Partite

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `POST` | `/api/v1/tornei/{torneoId}/partite/genera-calendario` | Genera il calendario round-robin |
| `GET` | `/api/v1/tornei/{torneoId}/partite` | Lista partite del torneo |
| `POST` | `/api/v1/partite/{partitaId}/risultato` | Inserisce o aggiorna un risultato |

### Classifica

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `GET` | `/api/v1/gironi/{gironeId}/classifica` | Classifica del girone (ordinata) |

### Admin

| Metodo | Endpoint | Descrizione |
|--------|----------|-------------|
| `DELETE` | `/api/v1/reset-db` | Azzera tutti i dati del database |

---

## Esempio d'uso via cURL (flusso completo)

```bash
BASE="http://127.0.0.1:8000/api/v1"

# 1. Crea un torneo
curl -X POST $BASE/tornei \
  -H "Content-Type: application/json" \
  -d '{"nome": "Torneo Primavera", "anno": 2026}'

# 2. Aggiungi squadre (sostituisci abc12345 con l'ID restituito)
curl -X POST $BASE/tornei/abc12345/squadre \
  -H "Content-Type: application/json" \
  -d '{"nome": "Aquile FC"}'

# 3. Lista giocatori di una squadra
curl $BASE/squadre/def67890/giocatori

# 4. Aggiungi un giocatore
curl -X POST $BASE/squadre/def67890/giocatori \
  -H "Content-Type: application/json" \
  -d '{"nome": "Mario", "cognome": "Rossi", "numero_maglia": 10}'

# 5. Genera i gironi
curl -X POST $BASE/tornei/abc12345/gironi/genera \
  -H "Content-Type: application/json" \
  -d '{"num_gironi": 2}'

# 6. Genera il calendario
curl -X POST $BASE/tornei/abc12345/partite/genera-calendario

# 7. Inserisci un risultato (sostituisci ghi11111 con l'ID partita)
curl -X POST $BASE/partite/ghi11111/risultato \
  -H "Content-Type: application/json" \
  -d '{"gol_casa": 3, "gol_ospite": 1}'

# 8. Leggi la classifica (sostituisci jkl22222 con l'ID girone)
curl $BASE/gironi/jkl22222/classifica
```

---

## Note tecniche

- I dati sono **persistenti**: salvati in `database.json` tramite TinyDB e ricaricati automaticamente al riavvio del server.
- Il sistema di punti segue il regolamento standard: **vittoria = 3 pt**, **pareggio = 1 pt**, **sconfitta = 0 pt**.
- La classifica è ordinata per: punti → differenza reti → gol fatti.
- È possibile **correggere un risultato** già inserito: la classifica viene aggiornata automaticamente.
- Il frontend usa **ES Modules** (`type="module"`): è necessario servirlo tramite un server HTTP (es. il server FastAPI incluso), non aprendo direttamente il file HTML nel browser.
