# main.py - Entry point FastAPI
# Avvio: uvicorn backend.main:app --reload

from pathlib import Path

from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import Any
from tinydb import TinyDB, Query

from backend import services

app = FastAPI(
    title="SGTC - Sistema di Gestione Tornei di Calcio Scolastici",
    description=(
        "Backend REST per la gestione di tornei di calcio scolastici.\n\n"
        "**Tiny DB**: tutti i dati sono salvati in un file database.json."
    ),
    version="1.1.5",
    contact={"name": "SGTC Gestione Tornei"},
)

# ── CORS (permetti tutte le origini in sviluppo) ──
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = TinyDB("database.json")

PREFIX = "/api/v1"


# ─────────────────────────────────────────────────────────────────────────────
# TORNEI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei", status_code=201, tags=["Tornei"])
async def crea_torneo(data: dict[str, Any] = Body(...)):
    """Crea un nuovo torneo. Body: `{"nome": "...", "anno": 2025}`"""
    return services.crea_torneo(data)


@app.get(f"{PREFIX}/tornei", tags=["Tornei"])
async def lista_tornei():
    """Restituisce tutti i tornei."""
    return services.lista_tornei()


@app.get(f"{PREFIX}/tornei/{{torneoID}}", tags=["Tornei"])
async def get_torneo(torneoID: str):
    """Restituisce un torneo per ID."""
    return services.get_torneo(torneoID)


@app.patch(f"{PREFIX}/tornei/{{torneoID}}", tags=["Tornei"])
async def aggiorna_torneo(torneoID: str, data: dict[str, Any] = Body(...)):
    """Aggiorna parzialmente un torneo. Campi modificabili: `nome`, `anno`, `stato`."""
    return services.aggiorna_torneo(torneoID, data)


@app.delete(f"{PREFIX}/tornei/{{torneoID}}", tags=["Tornei"])
async def elimina_torneo(torneoID: str):
    """Elimina un torneo per ID."""
    return services.elimina_torneo(torneoID)


# ─────────────────────────────────────────────────────────────────────────────
# SQUADRE
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoID}}/squadre", status_code=201, tags=["Squadre"])
async def crea_squadra(torneoID: str, data: dict[str, Any] = Body(...)):
    """Aggiunge una squadra a un torneo. Body: `{"nome": "..."}`"""
    return services.crea_squadra(torneoID, data)


@app.get(f"{PREFIX}/tornei/{{torneoID}}/squadre", tags=["Squadre"])
async def lista_squadre(torneoID: str):
    """Lista tutte le squadre di un torneo."""
    return services.lista_squadre(torneoID)


# ─────────────────────────────────────────────────────────────────────────────
# GIOCATORI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/squadre/{{squadraId}}/giocatori", status_code=201, tags=["Giocatori"])
async def crea_giocatore(squadraId: str, data: dict[str, Any] = Body(...)):
    """Aggiunge un giocatore a una squadra. Body: `{"nome": "...", "cognome": "...", "numero_maglia": 10}`"""
    return services.crea_giocatore(squadraId, data)


@app.get(f"{PREFIX}/squadre/{{squadraId}}/giocatori", tags=["Giocatori"])
async def lista_giocatori(squadraId: str):
    """Lista tutti i giocatori di una squadra."""
    return services.lista_giocatori(squadraId)


@app.delete(f"{PREFIX}/squadre/{{squadraId}}/giocatori/{{giocatoreId}}", tags=["Giocatori"])
async def elimina_giocatore(squadraId: str, giocatoreId: str):
    """Rimuove un giocatore da una squadra."""
    return services.elimina_giocatore(squadraId, giocatoreId)


# ─────────────────────────────────────────────────────────────────────────────
# GIRONI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoID}}/gironi/genera", status_code=201, tags=["Gironi"])
async def genera_gironi(torneoID: str, data: dict[str, Any] = Body(...)):
    """
    Genera i gironi distribuendo le squadre in modo bilanciato.
    Body: `{"num_gironi": 2}`
    """
    return services.genera_gironi(torneoID, data)


@app.get(f"{PREFIX}/tornei/{{torneoID}}/gironi", tags=["Gironi"])
async def lista_gironi(torneoID: str):
    """Lista tutti i gironi di un torneo."""
    return services.lista_gironi(torneoID)


# ─────────────────────────────────────────────────────────────────────────────
# PARTITE
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoID}}/partite/genera-calendario", status_code=201, tags=["Partite"])
async def genera_calendario(torneoID: str):
    """Genera il calendario round-robin per ogni girone del torneo."""
    return services.genera_calendario(torneoID)


@app.get(f"{PREFIX}/tornei/{{torneoID}}/partite", tags=["Partite"])
async def lista_partite(torneoID: str):
    """Lista tutte le partite di un torneo."""
    return services.lista_partite(torneoID)


@app.post(f"{PREFIX}/partite/{{partitaID}}/risultato", tags=["Partite"])
async def inserisci_risultato(partitaID: str, data: dict[str, Any] = Body(...)):
    """
    Inserisce o aggiorna il risultato di una partita. Aggiorna automaticamente la classifica.
    Body: `{"gol_casa": 2, "gol_ospite": 1}`
    """
    return services.inserisci_risultato(partitaID, data)


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFICA
# ─────────────────────────────────────────────────────────────────────────────

@app.get(f"{PREFIX}/gironi/{{gironeID}}/classifica", tags=["Classifica"])
async def get_classifica(gironeID: str):
    """Restituisce la classifica di un girone, ordinata per punti."""
    return services.get_classifica(gironeID)

# ─────────────────────────────────────────────────────────────────────────────
# RESET DB
# ─────────────────────────────────────────────────────────────────────────────

@app.delete(f"{PREFIX}/reset-db", tags=["Reset DB"])
async def reset_db():
    """Resetta tutti i dati del database. **Attenzione: questa operazione è irreversibile!**"""
    services.query_cancellare_dati_db()
    return {"message": "Database resettato con successo"}


# ── STATIC FILES (frontend) — montato DOPO le rotte API ──
_frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if _frontend_dir.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dir), html=True), name="frontend")