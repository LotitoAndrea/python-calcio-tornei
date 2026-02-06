# Tappa 1 — Contratto API (OpenAPI-first)
Progetto: **Sistema di Gestione Tornei di Calcio (SGTC)**  
Versione: v1  
Base path: `/api/v1`

---

## 1. Obiettivo
Definire il **contratto API REST** del backend del sistema di gestione tornei di calcio, in allineamento con:
- Requisiti funzionali (Tappa 0)
- Diagramma UML delle classi
- Modello ER

L’approccio adottato è **OpenAPI-first**: prima si definiscono endpoint, payload e regole, poi si implementa il codice.

---

## 2. Risorse principali
- Torneo
- Squadra
- Giocatore
- Fase
- Girone
- Partita
- IscrizioneGirone
- Classifica (derivata)

---

## 3. Endpoint REST principali

### 3.1 Tornei (CRUD)
- POST `/tornei`
- GET `/tornei`
- GET `/tornei/{torneoId}`
- PATCH `/tornei/{torneoId}`
- DELETE `/tornei/{torneoId}`

### 3.2 Squadre (CRUD, legate al torneo)
- POST `/tornei/{torneoId}/squadre`
- GET `/tornei/{torneoId}/squadre`
- GET `/squadre/{squadraId}`
- PATCH `/squadre/{squadraId}`
- DELETE `/squadre/{squadraId}`

### 3.3 Giocatori (iscrizione a squadra)
- POST `/squadre/{squadraId}/giocatori`
- DELETE `/squadre/{squadraId}/giocatori/{giocatoreId}`

### 3.4 Gironi
- POST `/tornei/{torneoId}/gironi/genera`
- GET `/tornei/{torneoId}/gironi`

### 3.5 Partite
- POST `/tornei/{torneoId}/partite/genera-calendario`
- GET `/tornei/{torneoId}/partite`
- POST `/partite/{partitaId}/risultato`

### 3.6 Classifiche
- GET `/tornei/{torneoId}/classifica`
- GET `/gironi/{gironeId}/classifica`

---

## 4. Endpoint chiave – Request & Response

### 4.1 Creazione torneo
**POST** `/tornei`

**Request**
```json
{
  "nome": "Torneo Calcetto Classi Quinte",
  "sport": "calcetto",
  "anniScolastici": "2025/2026",
  "giocatoriInCampo": 6,
  "minAnnoNascita": 2007,
  "maxAnnoNascita": 2009,
  "dataInizio": "2026-03-10",
  "dataFine": "2026-04-10"
}
```

**Response – 201 Created**
```json
{
  "idTorneo": "t1",
  "nome": "Torneo Calcetto Classi Quinte",
  "stato": "CREATO"
}
```

**Errori**
- 400 Bad Request – campi mancanti
- 422 Unprocessable Entity – formato non valido

---

### 4.2 Creazione squadra
**POST** `/tornei/{torneoId}/squadre`

**Request**
```json
{
  "nomeSquadra": "5A",
  "classe": "5A",
  "sezione": "Meccanica"
}
```

**Response – 201**
```json
{
  "idSquadra": "s10",
  "nomeSquadra": "5A",
  "torneoId": "t1"
}
```

---

### 4.3 Aggiunta giocatore a squadra
**POST** `/squadre/{squadraId}/giocatori`

**Request**
```json
{
  "nome": "Luca",
  "cognome": "Bianchi",
  "annoNascita": 2008,
  "ruolo": "Attaccante"
}
```

**Regole**
- `annoNascita` deve rientrare nei limiti del torneo

---

### 4.4 Generazione gironi
**POST** `/tornei/{torneoId}/gironi/genera`

**Request**
```json
{
  "dimensioneGironeMin": 3,
  "dimensioneGironeMax": 6,
  "shuffle": true
}
```

---

### 4.5 Generazione calendario partite
**POST** `/tornei/{torneoId}/partite/genera-calendario`

**Request**
```json
{
  "tipo": "GIRONI",
  "campiDisponibili": ["Campo 1", "Campo 2"],
  "durataMinuti": 20
}
```

---

### 4.6 Inserimento risultato partita
**POST** `/partite/{partitaId}/risultato`

**Request**
```json
{
  "goalCasa": 2,
  "goalOspite": 1
}
```

---

### 4.7 Lettura classifica girone
**GET** `/gironi/{gironeId}/classifica`

**Response – 200**
```json
{
  "gironeId": "gA",
  "classifica": [
    {
      "nomeSquadra": "5A",
      "punti": 6,
      "goalFatti": 5,
      "goalSubiti": 2,
      "differenzaReti": 3
    }
  ]
}
```

---

## 5. Tabella riassuntiva endpoint

| Metodo | Path | Descrizione |
|------|------|------------|
| POST | /tornei | Crea torneo |
| GET | /tornei | Lista tornei |
| POST | /tornei/{id}/squadre | Crea squadra |
| POST | /squadre/{id}/giocatori | Aggiunge giocatore |
| POST | /tornei/{id}/gironi/genera | Genera gironi |
| POST | /tornei/{id}/partite/genera-calendario | Genera calendario |
| POST | /partite/{id}/risultato | Inserisce risultato |
| GET | /gironi/{id}/classifica | Legge classifica |

---

## 6. Note di allineamento UML
- Ogni endpoint è mappato a una classe UML
- Le relazioni UML determinano i path nidificati
- La classifica è una vista derivata da Partita + IscrizioneGirone

---

## 7. Output di consegna
Questo documento costituisce il **contratto API** e sarà utilizzato come base per:
- definizione OpenAPI (Swagger)
- implementazione backend (FastAPI)
