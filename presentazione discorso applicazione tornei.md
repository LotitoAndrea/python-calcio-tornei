# Presentazione — Sistema di Gestione Tornei di Calcio (SGTC)

**Gruppo:** Andrea, Gabriel, Riccardo

---

## Scaletta presentazione

| # | Argomento | Chi parla |
|---|-----------|-----------|
| 1 | UML — Diagramma delle classi | Andrea, Gabriel |
| 2 | Contratto API REST (documento) | Andrea, Riccardo |
| 3 | Implementazione API con FastAPI | Andrea |
| 4 | Persistenza dati con TinyDB | Riccardo, Gabriel |
| 5 | Demo live — `/docs` + Frontend | tutti |

---

## 1. UML — Diagramma delle classi
**Chi parla: Andrea, Gabriel**

### Cosa spiegare
- Il progetto gestisce tornei di calcio scolastici: squadre, giocatori, fasi, gironi e partite.
- Mostrare le **entità principali** e le loro relazioni:
  - `Torneo` → ha molte `Squadre` e molte `Fasi`
  - `Squadra` → ha molti `Giocatori`
  - `Fase` → può contenere `Gironi` (fase a gironi) o partite a eliminazione diretta
  - `Girone` → collegato alle squadre tramite `IscrizioneGirone` (entità associativa con punti, goal fatti/subiti)
  - `Partita` → appartiene a una `Fase`, ha una squadra casa e una ospite

### Punti da sottolineare
- `IscrizioneGirone` è un'entità **associativa**: tiene traccia di punti, goal fatti, goal subiti e differenza reti per ogni squadra nel proprio girone.
- Cardinalità chiave: un torneo può avere **0..N** squadre; ogni squadra appartiene a **1** solo torneo.
- `goalCasa`, `goalOspite`, `esito` sono attributi di `Partita` — il risultato è modellato dentro la partita stessa.

---

## 2. Contratto API REST — Documento
**Chi parla: Andrea, Riccardo**

### Cosa spiegare
- Prima di scrivere codice abbiamo seguito l'approccio **OpenAPI-first**: definire il contratto API (endpoint, payload, response) prima di implementare.
- Il documento `FASE1_tappa1_Contratto_API_Tornei_Calcio.md` descrive tutte le risorse e le operazioni.

### Risorse REST principali
- **Tornei** — `POST/GET/PATCH/DELETE /api/v1/tornei`
- **Squadre** — `POST/GET /api/v1/tornei/{torneoId}/squadre`
- **Giocatori** — `POST/DELETE /api/v1/squadre/{squadraId}/giocatori`
- **Gironi** — `POST /api/v1/tornei/{torneoId}/gironi/genera`
- **Partite** — `POST /api/v1/tornei/{torneoId}/partite/genera-calendario`
- **Risultati** — `POST /api/v1/partite/{partitaId}/risultato`
- **Classifiche** — `GET /api/v1/tornei/{torneoId}/classifica`

### Punti da sottolineare
- Ogni risorsa segue la convenzione REST: URL gerarchici, verbi HTTP corretti (POST per creare, GET per leggere, PATCH per aggiornare, DELETE per eliminare).
- Le operazioni di generazione (gironi, calendario) usano endpoint **azione** (`/genera`, `/genera-calendario`) perché non sono semplici CRUD.
- Gli ID sono generati lato server (UUID) — il client non li specifica mai nella creazione.

---

## 3. Implementazione API con FastAPI
**Chi parla: Andrea**

### Cosa spiegare
- Il backend è scritto in **Python** con il framework **FastAPI**.
- Il file principale è `backend/main.py`: definisce tutte le route e collega la logica di business.
- La logica applicativa è separata in `backend/services.py` (principio di separazione delle responsabilità).

### Struttura del codice
```
backend/
├── main.py       → route FastAPI (endpoint HTTP)
├── services.py   → logica di business (sorteggio, calcolo classifica, ecc.)
└── store.py      → accesso al database TinyDB
```

### Come funziona FastAPI
- Ogni endpoint è una funzione Python decorata con `@app.get(...)`, `@app.post(...)`, ecc.
- FastAPI genera automaticamente la documentazione interattiva su `/docs` (Swagger UI).
- Il middleware **CORS** permette al frontend JavaScript di chiamare il backend senza blocchi.

### Esempio di endpoint — Creazione torneo
```python
@app.post("/api/v1/tornei", status_code=201, tags=["Tornei"])
async def crea_torneo(data: dict[str, Any] = Body(...)):
    """Crea un nuovo torneo."""
    return services.crea_torneo(data)
```

### Punti da sottolineare
- FastAPI valida automaticamente i tipi e restituisce errori 422 se il payload è malformato.
- I tag (`tags=["Tornei"]`) raggruppano gli endpoint nella documentazione `/docs`.
- Il prefisso `/api/v1` in tutti gli URL permette di fare versioning dell'API in futuro.

---

## 4. Persistenza dati con TinyDB
**Chi parla: Riccardo, Gabriel**

### Cosa spiegare
- Al posto di un database tradizionale (PostgreSQL, MySQL) usiamo **TinyDB**, un database documentale leggero che salva tutto in un file JSON (`database.json`).
- È la scelta giusta per un progetto scolastico: nessun server da installare, il database è un semplice file leggibile.

### Come funziona TinyDB
```python
from tinydb import TinyDB, Query

db = TinyDB("database.json")
tornei_table = db.table("tornei")

# Inserimento
tornei_table.insert({"id": "uuid...", "nome": "Torneo Quinte"})

# Ricerca
Q = Query()
tornei_table.search(Q.id == "uuid...")
```

### Struttura del `database.json`
- Ogni **tabella** corrisponde a una risorsa: `tornei`, `squadre`, `giocatori`, `gironi`, `partite`, `iscrizioni`.
- I dati sono documenti JSON — flessibili, senza schema rigido.
- Ogni record ha un campo `id` (UUID) generato da `services.py` al momento della creazione.

### Punti da sottolineare
- TinyDB non ha transazioni: per operazioni complesse (es. genera gironi + iscrizioni) la logica è gestita in `services.py`.
- Il file `database.json` è persistente: i dati sopravvivono al riavvio del server.
- In un progetto reale si passerebbe a PostgreSQL o SQLite con SQLAlchemy, ma la struttura del codice rimarrebbe la stessa grazie alla separazione `services` / `store`.

---

## 5. Demo live
**Chi parla: tutti**

### Passo 1 — Avvio del server
```bash
.venv\Scripts\activate
uvicorn backend.main:app --reload
```
Il server parte su `http://127.0.0.1:8000`.

### Passo 2 — Documentazione interattiva `/docs`
Aprire `http://127.0.0.1:8000/docs` e mostrare:
- [ ] **POST /api/v1/tornei** — creare un torneo
- [ ] **POST /api/v1/tornei/{torneoId}/squadre** — aggiungere squadre
- [ ] **POST /api/v1/squadre/{squadraId}/giocatori** — aggiungere giocatori
- [ ] **POST /api/v1/tornei/{torneoId}/gironi/genera** — sorteggio gironi
- [ ] **POST /api/v1/tornei/{torneoId}/partite/genera-calendario** — genera calendario
- [ ] **POST /api/v1/partite/{partitaId}/risultato** — inserire un risultato
- [ ] **GET /api/v1/tornei/{torneoId}/classifica** — vedere la classifica aggiornata

### Passo 3 — Frontend
Aprire `http://127.0.0.1:8000` e mostrare:
- [ ] Homepage: lista tornei, creazione di un nuovo torneo
- [ ] Pagina torneo: aggiunta squadre, sorteggio gironi, calendario partite
- [ ] Inserimento risultati e aggiornamento classifica in tempo reale
- [ ] Pagina squadra: rosa giocatori

### Messaggio chiave da trasmettere
> Il sistema funziona end-to-end: dal documento UML, al contratto API, all'implementazione FastAPI con TinyDB, fino all'interfaccia web — tutto il flusso di un torneo è gestito dall'applicazione.
