# TEST MANUALI — SGTC (Sistema di Gestione Tornei di Calcio Scolastici)

## Come usare questa guida

1. Avvia il server:
   ```
   uvicorn backend.main:app --reload
   ```
2. Apri il browser su: http://127.0.0.1:8000/docs
3. Segui i test in ordine.
4. Ad ogni step che restituisce un ID, copialo e usalo nei passi successivi.

---

## VARIABILI DA ANNOTARE DURANTE I TEST

Tieniti pronto ad annotare questi valori man mano che li ottieni:

| Variabile        | Valore da annotare |
|------------------|--------------------|
| {torneoId}       | c6eb47d2           |
| {torneoIdVuoto}  | ec8efddc           |
| {squadraId1}     | b6a4d167           |
| {squadraId2}     | 4b0087e0           |
| {squadraId3}     | 0cefd4be           |
| {squadraId4}     | 8cf216f0           |
| {giocatoreId}    | f89ec899           |
| {giocatoreId2}   | e2eac94e           |
| {gironeId_A}     | b740524c           |
| {gironeId_B}     | b0d26e0f           |
| {partitaId}      | dde1368f           |
---

## FASE 1 — TORNEI V

### Test 1 — Crea un torneo V

Endpoint : POST /api/v1/tornei
Body     :
  {
    "nome": "Torneo Primavera 2025",
    "anno": 2025
  }

Output atteso (status 201):
  {
    "id": "a1b2c3d4",
    "nome": "Torneo Primavera 2025",
    "anno": 2025,
    "stato": "aperto"
  }

>> Annota il valore di "id" come {torneoId}

---

### Test 2 — Lista tutti i tornei V

Endpoint : GET /api/v1/tornei
Body     : nessuno

Output atteso (status 200):
  [
    {
      "id": "{torneoId}",
      "nome": "Torneo Primavera 2025",
      "anno": 2025,
      "stato": "aperto"
    }
  ]

---

### Test 3 — Dettaglio torneo V

Endpoint : GET /api/v1/tornei/{torneoId}
Body     : nessuno

Output atteso (status 200):
  {
    "id": "{torneoId}",
    "nome": "Torneo Primavera 2025",
    "anno": 2025,
    "stato": "aperto"
  }

---

### Test 4 — Aggiorna torneo (PATCH parziale) V

Endpoint : PATCH /api/v1/tornei/{torneoId}
Body     :
  {
    "stato": "in_corso"
  }

Output atteso (status 200):
  {
    "id": "{torneoId}",
    "nome": "Torneo Primavera 2025",
    "anno": 2025,
    "stato": "in_corso"
  }

---

### Test 5 — Torneo inesistente (errore atteso) V

Endpoint : GET /api/v1/tornei/aaaaaaaa
Body     : nessuno

Output atteso (status 404):
  {
    "detail": "Torneo 'aaaaaaaa' non trovato"
  }

---

### Test 6 — Crea un torneo vuoto (usato dopo per test errore gironi) V

Endpoint : POST /api/v1/tornei
Body     :
  {
    "nome": "Torneo Vuoto",
    "anno": 2025
  }

Output atteso (status 201):
  {
    "id": "xxxxxxxx",
    ...
  }

>> Annota il valore di "id" come {torneoIdVuoto}

---

## FASE 2 — SQUADRE V

### Test 7 — Crea squadra 1 V

Endpoint : POST /api/v1/tornei/{torneoId}/squadre
Body     :
  {
    "nome": "Aquile FC"
  }

Output atteso (status 201):
  {
    "id": "bbbbbbbb",
    "nome": "Aquile FC",
    "torneo_id": "{torneoId}",
    "giocatori": []
  }

>> Annota il valore di "id" come {squadraId1}

---

### Test 8 — Crea squadra 2 V

Endpoint : POST /api/v1/tornei/{torneoId}/squadre
Body     :
  {
    "nome": "Leoni SC"
  }

Output atteso (status 201):
  {
    "id": "cccccccc",
    "nome": "Leoni SC",
    "torneo_id": "{torneoId}",
    "giocatori": []
  }

>> Annota il valore di "id" come {squadraId2}

---

### Test 9 — Crea squadra 3 V

Endpoint : POST /api/v1/tornei/{torneoId}/squadre
Body     :
  {
    "nome": "Tigri United"
  }

>> Annota il valore di "id" come {squadraId3}

---

### Test 10 — Crea squadra 4 V

Endpoint : POST /api/v1/tornei/{torneoId}/squadre
Body     :
  {
    "nome": "Falchi CF"
  }

>> Annota il valore di "id" come {squadraId4}

---

### Test 11 — Lista squadre del torneo V

Endpoint : GET /api/v1/tornei/{torneoId}/squadre
Body     : nessuno

Output atteso (status 200):
  Array con 4 squadre:
  [
    { "id": "{squadraId1}", "nome": "Aquile FC", ... },
    { "id": "{squadraId2}", "nome": "Leoni SC", ... },
    { "id": "{squadraId3}", "nome": "Tigri United", ... },
    { "id": "{squadraId4}", "nome": "Falchi CF", ... }
  ]

---

## FASE 3 — GIOCATORI V

### Test 12 — Aggiungi giocatore alla squadra 1 V

Endpoint : POST /api/v1/squadre/{squadraId1}/giocatori
Body     :
  {
    "nome": "Mario",
    "cognome": "Rossi",
    "numero_maglia": 10
  }

Output atteso (status 201):
  {
    "id": "dddddddd",
    "nome": "Mario",
    "cognome": "Rossi",
    "numero_maglia": 10,
    "squadra_id": "{squadraId1}"
  }

>> Annota il valore di "id" come {giocatoreId}

---

### Test 13 — Aggiungi secondo giocatore alla squadra 1 V

Endpoint : POST /api/v1/squadre/{squadraId1}/giocatori
Body     :
  {
    "nome": "Luca",
    "cognome": "Bianchi",
    "numero_maglia": 7
  }

Output atteso (status 201):
  {
    "id": "eeeeeeee",
    "nome": "Luca",
    "cognome": "Bianchi",
    "numero_maglia": 7,
    "squadra_id": "{squadraId1}"
  }

>> Annota il valore di "id" come {giocatoreId2}

---

### Test 14 — Verifica che i giocatori siano nella squadra V

Endpoint : GET /api/v1/tornei/{torneoId}/squadre
Body     : nessuno

Output atteso (status 200):
  La squadra "Aquile FC" deve avere:
  "giocatori": ["{giocatoreId}", "{giocatoreId2}"]

---

### Test 15 — Elimina il secondo giocatore V

Endpoint : DELETE /api/v1/squadre/{squadraId1}/giocatori/{giocatoreId2}
Body     : nessuno

Output atteso (status 200):
  {
    "message": "Giocatore '{giocatoreId2}' eliminato con successo"
  }

---

### Test 16 — Elimina giocatore dalla squadra sbagliata (errore atteso) V

Endpoint : DELETE /api/v1/squadre/{squadraId2}/giocatori/{giocatoreId}
Body     : nessuno

Output atteso (status 404):
  {
    "detail": "Giocatore '{giocatoreId}' non trovato in questa squadra"
  }

---

### Test 17 — Giocatore senza cognome (errore atteso) V

Endpoint : POST /api/v1/squadre/{squadraId1}/giocatori
Body     :
  {
    "nome": "Carlo"
  }

Output atteso (status 400):
  {
    "detail": "I campi 'nome' e 'cognome' sono obbligatori"
  }

---

## FASE 4 — GIRONI V

### Test 18 — Genera gironi (errore torneo vuoto) V

Endpoint : POST /api/v1/tornei/{torneoIdVuoto}/gironi/genera
Body     :
  {
    "num_gironi": 2
  }

Output atteso (status 400):
  {
    "detail": "Servono almeno 2 squadre per generare i gironi"
  }

---

### Test 19 — Genera gironi (torneo con 4 squadre) V

Endpoint : POST /api/v1/tornei/{torneoId}/gironi/genera
Body     :
  {
    "num_gironi": 2
  }

Output atteso (status 201):
  Array con 2 gironi:
  [
    {
      "id": "ffffffff",
      "torneo_id": "{torneoId}",
      "nome": "Girone A",
      "squadre": ["{squadraId1}", "{squadraId3}"]
    },
    {
      "id": "gggggggg",
      "torneo_id": "{torneoId}",
      "nome": "Girone B",
      "squadre": ["{squadraId2}", "{squadraId4}"]
    }
  ]

>> Annota i valori di "id" come {gironeId_A} e {gironeId_B}

---

### Test 20 — Lista gironi del torneo V

Endpoint : GET /api/v1/tornei/{torneoId}/gironi
Body     : nessuno

Output atteso (status 200):
  Array con i 2 gironi creati al test precedente.

---

## FASE 5 — PARTITE V

### Test 21 — Genera calendario (errore torneo senza gironi) V

Endpoint : POST /api/v1/tornei/{torneoIdVuoto}/partite/genera-calendario
Body     : nessuno

Output atteso (status 400):
  {
    "detail": "Nessun girone trovato. Genera prima i gironi con POST /gironi/genera"
  }

---

### Test 22 — Genera calendario partite V

Endpoint : POST /api/v1/tornei/{torneoId}/partite/genera-calendario
Body     : nessuno

Output atteso (status 201):
  Array con 2 partite (1 per girone, dato che ogni girone ha 2 squadre):
  [
    {
      "id": "hhhhhhhh",
      "torneo_id": "{torneoId}",
      "girone_id": "{gironeId_A}",
      "girone_nome": "Girone A",
      "squadra_casa_id": "{squadraId1}",
      "squadra_casa_nome": "Aquile FC",
      "squadra_ospite_id": "{squadraId3}",
      "squadra_ospite_nome": "Tigri United",
      "gol_casa": null,
      "gol_ospite": null,
      "giocata": false
    },
    { ... seconda partita del Girone B ... }
  ]

>> Annota il valore di "id" della prima partita come {partitaId}

---

### Test 23 — Lista partite del torneo V

Endpoint : GET /api/v1/tornei/{torneoId}/partite
Body     : nessuno

Output atteso (status 200):
  Array con 2 partite, entrambe con "giocata": false

---

## FASE 6 — RISULTATI E CLASSIFICA V

### Test 24 — Inserisci risultato (vittoria casa) V

Endpoint : POST /api/v1/partite/{partitaId}/risultato
Body     :
  {
    "gol_casa": 3,
    "gol_ospite": 1
  }

Output atteso (status 200):
  {
    "id": "{partitaId}",
    "gol_casa": 3,
    "gol_ospite": 1,
    "giocata": true,
    ...
  }

---

### Test 25 — Leggi classifica Girone A (dopo vittoria) V

Endpoint : GET /api/v1/gironi/{gironeId_A}/classifica
Body     : nessuno

Output atteso (status 200):
  [
    {
      "posizione": 1,
      "squadra_nome": "Aquile FC",
      "punti": 3,
      "vittorie": 1,
      "pareggi": 0,
      "sconfitte": 0,
      "gol_fatti": 3,
      "gol_subiti": 1,
      "differenza_reti": 2,
      "partite_giocate": 1
    },
    {
      "posizione": 2,
      "squadra_nome": "Tigri United",
      "punti": 0,
      "vittorie": 0,
      "pareggi": 0,
      "sconfitte": 1,
      "gol_fatti": 1,
      "gol_subiti": 3,
      "differenza_reti": -2,
      "partite_giocate": 1
    }
  ]

---

### Test 26 — Correggi il risultato (pareggio) V

Endpoint : POST /api/v1/partite/{partitaId}/risultato
Body     :
  {
    "gol_casa": 2,
    "gol_ospite": 2
  }

Output atteso (status 200):
  {
    "gol_casa": 2,
    "gol_ospite": 2,
    "giocata": true,
    ...
  }

---

### Test 27 — Leggi classifica Girone A (dopo correzione) V

Endpoint : GET /api/v1/gironi/{gironeId_A}/classifica
Body     : nessuno

Output atteso (status 200):
  [
    {
      "posizione": 1,
      "squadra_nome": "Aquile FC",
      "punti": 1,
      "vittorie": 0,
      "pareggi": 1,
      "sconfitte": 0,
      "gol_fatti": 2,
      "gol_subiti": 2,
      "differenza_reti": 0,
      "partite_giocate": 1
    },
    {
      "posizione": 2,
      "squadra_nome": "Tigri United",
      "punti": 1,
      "vittorie": 0,
      "pareggi": 1,
      "sconfitte": 0,
      "gol_fatti": 2,
      "gol_subiti": 2,
      "differenza_reti": 0,
      "partite_giocate": 1
    }
  ]

  >> Entrambe con 1 punto: il ricalcolo automatico ha funzionato.

---

### Test 28 — Risultato con gol negativi (errore atteso) V

Endpoint : POST /api/v1/partite/{partitaId}/risultato
Body     :
  {
    "gol_casa": -1,
    "gol_ospite": 2
  }

Output atteso (status 400):
  {
    "detail": "I gol non possono essere negativi"
  }

---

### Test 29 — Risultato senza campo obbligatorio (errore atteso) V

Endpoint : POST /api/v1/partite/{partitaId}/risultato
Body     :
  {
    "gol_casa": 2
  }

Output atteso (status 400):
  {
    "detail": "I campi 'gol_casa' e 'gol_ospite' sono obbligatori"
  }

---

### Test 30 — Partita inesistente (errore atteso) V

Endpoint : POST /api/v1/partite/zzzzzzzz/risultato
Body     :
  {
    "gol_casa": 1,
    "gol_ospite": 0
  }

Output atteso (status 404):
  {
    "detail": "Partita 'zzzzzzzz' non trovata"
  }

---

## FASE 7 — ELIMINAZIONE V

### Test 31 — Elimina il torneo V

Endpoint : DELETE /api/v1/tornei/{torneoId}
Body     : nessuno

Output atteso (status 200):
  {
    "message": "Torneo '{torneoId}' eliminato con successo"
  }

---

### Test 32 — Torneo eliminato non più raggiungibile V

Endpoint : GET /api/v1/tornei/{torneoId}
Body     : nessuno

Output atteso (status 404):
  {
    "detail": "Torneo '{torneoId}' non trovato"
  }

---

## RIEPILOGO ORDINE DI ESECUZIONE

  1.  Crea torneo principale          →  salva {torneoId}
  2.  Crea torneo vuoto               →  salva {torneoIdVuoto}
  3.  Crea 4 squadre                  →  salva {squadraId1..4}
  4.  Aggiungi giocatori              →  salva {giocatoreId}, {giocatoreId2}
  5.  Elimina giocatore               →  verifica rimozione
  6.  Test errori giocatori           →  verifica 400 / 404
  7.  Genera gironi (errore vuoto)    →  verifica 400
  8.  Genera gironi                   →  salva {gironeId_A}, {gironeId_B}
  9.  Genera calendario (errore)      →  verifica 400
  10. Genera calendario               →  salva {partitaId}
  11. Inserisci risultato             →  verifica classifica aggiornata
  12. Correggi risultato              →  verifica ricalcolo classifica
  13. Test errori risultati           →  verifica 400 / 404
  14. Elimina torneo                  →  verifica 404

---

## SISTEMA DI PUNTEGGIO (promemoria)

  Vittoria  = 3 punti
  Pareggio  = 1 punto
  Sconfitta = 0 punti

  Ordine classifica: Punti > Differenza reti > Gol fatti
