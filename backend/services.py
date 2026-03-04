# services.py - Logica di business
# Tutte le operazioni sui dati passano da qui.

import uuid
from fastapi import HTTPException
from tinydb import TinyDB, Query

from backend import store


# ─────────────────────────────────────────────────────────────────────────────
# Utility
# ─────────────────────────────────────────────────────────────────────────────

db = TinyDB("database.json")

# Tabelle separate per ogni tipo di entità
_tornei_table      = db.table("tornei")
_squadre_table     = db.table("squadre")
_giocatori_table   = db.table("giocatori")
_gironi_table      = db.table("gironi")
_partite_table     = db.table("partite")
_classifiche_table = db.table("classifiche")

Q = Query()  # istanza condivisa per le query


def _new_id() -> str:
    """Genera un ID breve univoco (8 caratteri esadecimali)."""
    return uuid.uuid4().hex[:8]


def carica_da_db() -> None:
    """Carica tutti i dati persistiti nel JSON e li rimette nello store in memoria."""
    for doc in _tornei_table.all():
        store.tornei[doc["id"]] = dict(doc)
    for doc in _squadre_table.all():
        store.squadre[doc["id"]] = dict(doc)
    for doc in _giocatori_table.all():
        store.giocatori[doc["id"]] = dict(doc)
    for doc in _gironi_table.all():
        store.gironi[doc["id"]] = dict(doc)
    for doc in _partite_table.all():
        store.partite[doc["id"]] = dict(doc)
    for doc in _classifiche_table.all():
        cl_key = f"{doc['girone_id']}_{doc['squadra_id']}"
        store.classifiche[cl_key] = dict(doc)


# Ripristina lo stato al caricamento del modulo
carica_da_db()


# ─────────────────────────────────────────────────────────────────────────────
# TORNEI
# ─────────────────────────────────────────────────────────────────────────────

def crea_torneo(data: dict) -> dict:
    if not data.get("nome"):
        raise HTTPException(status_code=400, detail="Il campo 'nome' è obbligatorio")
    torneo_id = _new_id()
    torneo = {
        "id": torneo_id,
        "nome": data["nome"],
        "anno": data.get("anno", 2025),
        "stato": "aperto",          # aperto | in_corso | terminato
    }
    store.tornei[torneo_id] = torneo
    _tornei_table.insert(torneo)
    return torneo


def lista_tornei() -> list:
    return list(store.tornei.values())


def get_torneo(torneo_id: str) -> dict:
    torneo = store.tornei.get(torneo_id)
    if not torneo:
        raise HTTPException(status_code=404, detail=f"Torneo '{torneo_id}' non trovato")
    return torneo


def aggiorna_torneo(torneo_id: str, data: dict) -> dict:
    torneo = get_torneo(torneo_id)
    for campo in ("nome", "anno", "stato"):
        if campo in data:
            torneo[campo] = data[campo]
    _tornei_table.upsert(torneo, Q.id == torneo_id)
    return torneo


def elimina_torneo(torneo_id: str) -> dict:
    get_torneo(torneo_id)
    del store.tornei[torneo_id]
    _tornei_table.remove(Q.id == torneo_id)
    return {"message": f"Torneo '{torneo_id}' eliminato con successo"}


# ─────────────────────────────────────────────────────────────────────────────
# SQUADRE
# ─────────────────────────────────────────────────────────────────────────────

def crea_squadra(torneo_id: str, data: dict) -> dict:
    get_torneo(torneo_id)
    if not data.get("nome"):
        raise HTTPException(status_code=400, detail="Il campo 'nome' è obbligatorio")
    squadra_id = _new_id()
    squadra = {
        "id": squadra_id,
        "nome": data["nome"],
        "torneo_id": torneo_id,
        "giocatori": [],
    }
    store.squadre[squadra_id] = squadra
    _squadre_table.insert(squadra)
    return squadra


def lista_squadre(torneo_id: str) -> list:
    get_torneo(torneo_id)
    return [s for s in store.squadre.values() if s["torneo_id"] == torneo_id]


def _get_squadra(squadra_id: str) -> dict:
    squadra = store.squadre.get(squadra_id)
    if not squadra:
        raise HTTPException(status_code=404, detail=f"Squadra '{squadra_id}' non trovata")
    return squadra


# ─────────────────────────────────────────────────────────────────────────────
# GIOCATORI
# ─────────────────────────────────────────────────────────────────────────────

def crea_giocatore(squadra_id: str, data: dict) -> dict:
    squadra = _get_squadra(squadra_id)
    if not data.get("nome") or not data.get("cognome"):
        raise HTTPException(status_code=400, detail="I campi 'nome' e 'cognome' sono obbligatori")
    giocatore_id = _new_id()
    giocatore = {
        "id": giocatore_id,
        "nome": data["nome"],
        "cognome": data["cognome"],
        "numero_maglia": data.get("numero_maglia"),
        "squadra_id": squadra_id,
    }
    store.giocatori[giocatore_id] = giocatore
    squadra["giocatori"].append(giocatore_id)
    _giocatori_table.insert(giocatore)
    # Aggiorna la lista giocatori della squadra nel DB
    _squadre_table.upsert(squadra, Q.id == squadra_id)
    return giocatore


def lista_giocatori(squadra_id: str) -> list:
    """Restituisce tutti i giocatori di una squadra dallo store in memoria."""
    _get_squadra(squadra_id)
    return [g for g in store.giocatori.values() if g["squadra_id"] == squadra_id]


def elimina_giocatore(squadra_id: str, giocatore_id: str) -> dict:
    squadra = _get_squadra(squadra_id)
    giocatore = store.giocatori.get(giocatore_id)
    if not giocatore or giocatore["squadra_id"] != squadra_id:
        raise HTTPException(
            status_code=404,
            detail=f"Giocatore '{giocatore_id}' non trovato in questa squadra",
        )
    squadra["giocatori"].remove(giocatore_id)
    _giocatori_table.remove(Q.id == giocatore_id)
    del store.giocatori[giocatore_id]
    # Aggiorna la lista giocatori della squadra nel DB
    _squadre_table.upsert(squadra, Q.id == squadra_id)
    return {"message": f"Giocatore '{giocatore_id}' eliminato con successo"}


# ─────────────────────────────────────────────────────────────────────────────
# GIRONI
# ─────────────────────────────────────────────────────────────────────────────

def genera_gironi(torneo_id: str, data: dict) -> list:
    get_torneo(torneo_id)
    squadre_torneo = lista_squadre(torneo_id)

    if len(squadre_torneo) < 2:
        raise HTTPException(status_code=400, detail="Servono almeno 2 squadre per generare i gironi")

    num_gironi = int(data.get("num_gironi", 2))
    if num_gironi < 1:
        raise HTTPException(status_code=400, detail="Il numero di gironi deve essere almeno 1")
    if num_gironi > len(squadre_torneo):
        raise HTTPException(
            status_code=400,
            detail=f"Numero di gironi ({num_gironi}) superiore alle squadre disponibili ({len(squadre_torneo)})",
        )

    # Pulizia: rimuove gironi, partite e classifiche precedenti per questo torneo
    _reset_torneo_data(torneo_id)

    LETTERE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    gironi_creati = []

    for i in range(num_gironi):
        girone_id = _new_id()
        # Distribuzione round-robin tra i gironi
        squadre_nel_girone = [s["id"] for j, s in enumerate(squadre_torneo) if j % num_gironi == i]
        girone = {
            "id": girone_id,
            "torneo_id": torneo_id,
            "nome": f"Girone {LETTERE[i % len(LETTERE)]}",
            "squadre": squadre_nel_girone,
        }
        store.gironi[girone_id] = girone
        _gironi_table.insert(girone)
        gironi_creati.append(girone)

        # Inizializza la classifica per ogni squadra del girone
        for s_id in squadre_nel_girone:
            cl_key = f"{girone_id}_{s_id}"
            voce = {
                "girone_id": girone_id,
                "torneo_id": torneo_id,
                "squadra_id": s_id,
                "squadra_nome": store.squadre[s_id]["nome"],
                "punti": 0,
                "partite_giocate": 0,
                "vittorie": 0,
                "pareggi": 0,
                "sconfitte": 0,
                "gol_fatti": 0,
                "gol_subiti": 0,
                "differenza_reti": 0,
            }
            store.classifiche[cl_key] = voce
            _classifiche_table.insert(voce)

    return gironi_creati


def lista_gironi(torneo_id: str) -> list:
    get_torneo(torneo_id)
    return [g for g in store.gironi.values() if g["torneo_id"] == torneo_id]


def _get_girone(girone_id: str) -> dict:
    girone = store.gironi.get(girone_id)
    if not girone:
        raise HTTPException(status_code=404, detail=f"Girone '{girone_id}' non trovato")
    return girone


def _reset_torneo_data(torneo_id: str) -> None:
    """Rimuove gironi, partite e classifiche esistenti per un torneo (store + DB)."""
    for g_id in [k for k, v in store.gironi.items() if v["torneo_id"] == torneo_id]:
        del store.gironi[g_id]
    for p_id in [k for k, v in store.partite.items() if v["torneo_id"] == torneo_id]:
        del store.partite[p_id]
    for cl_key in [k for k, v in store.classifiche.items() if v["torneo_id"] == torneo_id]:
        del store.classifiche[cl_key]
    # Pulizia DB
    _gironi_table.remove(Q.torneo_id == torneo_id)
    _partite_table.remove(Q.torneo_id == torneo_id)
    _classifiche_table.remove(Q.torneo_id == torneo_id)


# ─────────────────────────────────────────────────────────────────────────────
# PARTITE
# ─────────────────────────────────────────────────────────────────────────────

def genera_calendario(torneo_id: str) -> list:
    get_torneo(torneo_id)
    gironi_torneo = lista_gironi(torneo_id)

    if not gironi_torneo:
        raise HTTPException(
            status_code=400,
            detail="Nessun girone trovato. Genera prima i gironi con POST /gironi/genera"
        )

    # Rimuove le partite precedenti (non le classifiche)
    for p_id in [k for k, v in store.partite.items() if v["torneo_id"] == torneo_id]:
        del store.partite[p_id]

    partite_create = []

    for girone in gironi_torneo:
        ids = girone["squadre"]
        # Round-robin: ogni coppia gioca una volta
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                partita_id = _new_id()
                partita = {
                    "id": partita_id,
                    "torneo_id": torneo_id,
                    "girone_id": girone["id"],
                    "girone_nome": girone["nome"],
                    "squadra_casa_id": ids[i],
                    "squadra_casa_nome": store.squadre[ids[i]]["nome"],
                    "squadra_ospite_id": ids[j],
                    "squadra_ospite_nome": store.squadre[ids[j]]["nome"],
                    "gol_casa": None,
                    "gol_ospite": None,
                    "giocata": False,
                }
                store.partite[partita_id] = partita
                _partite_table.insert(partita)
                partite_create.append(partita)

    return partite_create


def lista_partite(torneo_id: str) -> list:
    get_torneo(torneo_id)
    return [p for p in store.partite.values() if p["torneo_id"] == torneo_id]


def inserisci_risultato(partita_id: str, data: dict) -> dict:
    partita = store.partite.get(partita_id)
    if not partita:
        raise HTTPException(status_code=404, detail=f"Partita '{partita_id}' non trovata")

    gol_casa = data.get("gol_casa")
    gol_ospite = data.get("gol_ospite")

    if gol_casa is None or gol_ospite is None:
        raise HTTPException(status_code=400, detail="I campi 'gol_casa' e 'gol_ospite' sono obbligatori")
    if not isinstance(gol_casa, int) or not isinstance(gol_ospite, int):
        raise HTTPException(status_code=400, detail="I gol devono essere numeri interi")
    if gol_casa < 0 or gol_ospite < 0:
        raise HTTPException(status_code=400, detail="I gol non possono essere negativi")

    # Se la partita era già stata giocata, annulla il risultato precedente
    if partita["giocata"]:
        _annulla_risultato_classifica(partita)

    partita["gol_casa"] = gol_casa
    partita["gol_ospite"] = gol_ospite
    partita["giocata"] = True

    _applica_risultato_classifica(partita)
    # Persiste la partita aggiornata
    _partite_table.upsert(partita, Q.id == partita_id)
    return partita


def _annulla_risultato_classifica(partita: dict) -> None:
    """Cancella l'effetto del risultato precedente dalla classifica."""
    g_id = partita["girone_id"]
    casa_id = partita["squadra_casa_id"]
    ospite_id = partita["squadra_ospite_id"]
    gol_c = partita["gol_casa"]
    gol_o = partita["gol_ospite"]

    cl_c = store.classifiche.get(f"{g_id}_{casa_id}")
    cl_o = store.classifiche.get(f"{g_id}_{ospite_id}")
    if not cl_c or not cl_o:
        return

    cl_c["partite_giocate"] -= 1
    cl_o["partite_giocate"] -= 1
    cl_c["gol_fatti"] -= gol_c
    cl_c["gol_subiti"] -= gol_o
    cl_o["gol_fatti"] -= gol_o
    cl_o["gol_subiti"] -= gol_c
    cl_c["differenza_reti"] = cl_c["gol_fatti"] - cl_c["gol_subiti"]
    cl_o["differenza_reti"] = cl_o["gol_fatti"] - cl_o["gol_subiti"]

    if gol_c > gol_o:
        cl_c["vittorie"] -= 1
        cl_c["punti"] -= 3
        cl_o["sconfitte"] -= 1
    elif gol_c < gol_o:
        cl_o["vittorie"] -= 1
        cl_o["punti"] -= 3
        cl_c["sconfitte"] -= 1
    else:
        cl_c["pareggi"] -= 1
        cl_c["punti"] -= 1
        cl_o["pareggi"] -= 1
        cl_o["punti"] -= 1


def _applica_risultato_classifica(partita: dict) -> None:
    """Applica il nuovo risultato alla classifica."""
    g_id = partita["girone_id"]
    casa_id = partita["squadra_casa_id"]
    ospite_id = partita["squadra_ospite_id"]
    gol_c = partita["gol_casa"]
    gol_o = partita["gol_ospite"]

    cl_c = store.classifiche.get(f"{g_id}_{casa_id}")
    cl_o = store.classifiche.get(f"{g_id}_{ospite_id}")
    if not cl_c or not cl_o:
        raise HTTPException(status_code=500, detail="Errore interno: voce di classifica mancante")

    cl_c["partite_giocate"] += 1
    cl_o["partite_giocate"] += 1
    cl_c["gol_fatti"] += gol_c
    cl_c["gol_subiti"] += gol_o
    cl_o["gol_fatti"] += gol_o
    cl_o["gol_subiti"] += gol_c
    cl_c["differenza_reti"] = cl_c["gol_fatti"] - cl_c["gol_subiti"]
    cl_o["differenza_reti"] = cl_o["gol_fatti"] - cl_o["gol_subiti"]

    if gol_c > gol_o:
        cl_c["vittorie"] += 1
        cl_c["punti"] += 3
        cl_o["sconfitte"] += 1
    elif gol_c < gol_o:
        cl_o["vittorie"] += 1
        cl_o["punti"] += 3
        cl_c["sconfitte"] += 1
    else:
        cl_c["pareggi"] += 1
        cl_c["punti"] += 1
        cl_o["pareggi"] += 1
        cl_o["punti"] += 1
    # Persiste le due voci di classifica aggiornate
    _classifiche_table.upsert(cl_c, (Q.girone_id == g_id) & (Q.squadra_id == casa_id))
    _classifiche_table.upsert(cl_o, (Q.girone_id == g_id) & (Q.squadra_id == ospite_id))


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFICA
# ─────────────────────────────────────────────────────────────────────────────

def get_classifica(girone_id: str) -> list:
    _get_girone(girone_id)      # verifica esistenza
    girone = store.gironi[girone_id]

    classifica = [
        store.classifiche[f"{girone_id}_{s_id}"]
        for s_id in girone["squadre"]
        if f"{girone_id}_{s_id}" in store.classifiche
    ]

    # Ordinamento: punti → differenza reti → gol fatti
    classifica.sort(key=lambda x: (-x["punti"], -x["differenza_reti"], -x["gol_fatti"]))

    # Aggiunge la posizione in classifica
    for pos, entry in enumerate(classifica, start=1):
        entry["posizione"] = pos

    return classifica

# ─────────────────────────────────────────────────────────────────────────────
# QUERY TINYDB  (lettura diretta dal file JSON)
# ─────────────────────────────────────────────────────────────────────────────

def query_tornei_per_anno(anno: int) -> list:
    """Restituisce tutti i tornei di un determinato anno."""
    return _tornei_table.search(Q.anno == anno)


def query_tornei_per_stato(stato: str) -> list:
    """Restituisce i tornei filtrati per stato (aperto | in_corso | terminato)."""
    return _tornei_table.search(Q.stato == stato)


def query_squadre_per_torneo(torneo_id: str) -> list:
    """Restituisce tutte le squadre di un torneo leggendo dal DB."""
    return _squadre_table.search(Q.torneo_id == torneo_id)


def query_giocatori_per_squadra(squadra_id: str) -> list:
    """Restituisce tutti i giocatori di una squadra leggendo dal DB."""
    return _giocatori_table.search(Q.squadra_id == squadra_id)


def query_partite_non_giocate(torneo_id: str) -> list:
    """Restituisce le partite ancora da giocare di un torneo."""
    return _partite_table.search((Q.torneo_id == torneo_id) & (Q.giocata == False))


def query_classifica_girone(girone_id: str) -> list:
    """Restituisce la classifica di un girone ordinata per punti (dal DB)."""
    voci = _classifiche_table.search(Q.girone_id == girone_id)
    return sorted(voci, key=lambda x: (-x["punti"], -x["differenza_reti"], -x["gol_fatti"]))

def query_cancellare_dati_db() -> None:
    """Cancella tutti i dati dal DB (per test/reset)."""
    _tornei_table.truncate()
    _squadre_table.truncate()
    _giocatori_table.truncate()
    _gironi_table.truncate()
    _partite_table.truncate()
    _classifiche_table.truncate()