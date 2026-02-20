# main.py - Entry point FastAPI
# Avvio: uvicorn app.main:app --reload

from fastapi import FastAPI, Request

from backend import services

app = FastAPI(
    title="SGTC - Sistema di Gestione Tornei di Calcio Scolastici",
    description=(
        "Backend REST per la gestione di tornei di calcio scolastici.\n\n"
        "**Nessun database**: tutti i dati sono conservati in memoria durante l'esecuzione."
    ),
    version="1.0.0",
    contact={"name": "SGTC School Project"},
)

PREFIX = "/api/v1"


# ─────────────────────────────────────────────────────────────────────────────
# TORNEI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei", status_code=201, tags=["Tornei"])
async def crea_torneo(request: Request):
    """Crea un nuovo torneo. Body: `{"nome": "...", "anno": 2025}`"""
    data = await request.json()
    return services.crea_torneo(data)


@app.get(f"{PREFIX}/tornei", tags=["Tornei"])
async def lista_tornei():
    """Restituisce tutti i tornei."""
    return services.lista_tornei()


@app.get(f"{PREFIX}/tornei/{{torneoId}}", tags=["Tornei"])
async def get_torneo(torneoId: str):
    """Restituisce un torneo per ID."""
    return services.get_torneo(torneoId)


@app.patch(f"{PREFIX}/tornei/{{torneoId}}", tags=["Tornei"])
async def aggiorna_torneo(torneoId: str, request: Request):
    """Aggiorna parzialmente un torneo. Campi modificabili: `nome`, `anno`, `stato`."""
    data = await request.json()
    return services.aggiorna_torneo(torneoId, data)


@app.delete(f"{PREFIX}/tornei/{{torneoId}}", tags=["Tornei"])
async def elimina_torneo(torneoId: str):
    """Elimina un torneo per ID."""
    return services.elimina_torneo(torneoId)


# ─────────────────────────────────────────────────────────────────────────────
# SQUADRE
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoId}}/squadre", status_code=201, tags=["Squadre"])
async def crea_squadra(torneoId: str, request: Request):
    """Aggiunge una squadra a un torneo. Body: `{"nome": "..."}`"""
    data = await request.json()
    return services.crea_squadra(torneoId, data)


@app.get(f"{PREFIX}/tornei/{{torneoId}}/squadre", tags=["Squadre"])
async def lista_squadre(torneoId: str):
    """Lista tutte le squadre di un torneo."""
    return services.lista_squadre(torneoId)


# ─────────────────────────────────────────────────────────────────────────────
# GIOCATORI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/squadre/{{squadraId}}/giocatori", status_code=201, tags=["Giocatori"])
async def crea_giocatore(squadraId: str, request: Request):
    """Aggiunge un giocatore a una squadra. Body: `{"nome": "...", "cognome": "...", "numero_maglia": 10}`"""
    data = await request.json()
    return services.crea_giocatore(squadraId, data)


@app.delete(f"{PREFIX}/squadre/{{squadraId}}/giocatori/{{giocatoreId}}", tags=["Giocatori"])
async def elimina_giocatore(squadraId: str, giocatoreId: str):
    """Rimuove un giocatore da una squadra."""
    return services.elimina_giocatore(squadraId, giocatoreId)


# ─────────────────────────────────────────────────────────────────────────────
# GIRONI
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoId}}/gironi/genera", status_code=201, tags=["Gironi"])
async def genera_gironi(torneoId: str, request: Request):
    """
    Genera i gironi distribuendo le squadre in modo bilanciato.
    Body: `{"num_gironi": 2}`
    """
    data = await request.json()
    return services.genera_gironi(torneoId, data)


@app.get(f"{PREFIX}/tornei/{{torneoId}}/gironi", tags=["Gironi"])
async def lista_gironi(torneoId: str):
    """Lista tutti i gironi di un torneo."""
    return services.lista_gironi(torneoId)


# ─────────────────────────────────────────────────────────────────────────────
# PARTITE
# ─────────────────────────────────────────────────────────────────────────────

@app.post(f"{PREFIX}/tornei/{{torneoId}}/partite/genera-calendario", status_code=201, tags=["Partite"])
async def genera_calendario(torneoId: str):
    """Genera il calendario round-robin per ogni girone del torneo."""
    return services.genera_calendario(torneoId)


@app.get(f"{PREFIX}/tornei/{{torneoId}}/partite", tags=["Partite"])
async def lista_partite(torneoId: str):
    """Lista tutte le partite di un torneo."""
    return services.lista_partite(torneoId)


@app.post(f"{PREFIX}/partite/{{partitaId}}/risultato", tags=["Partite"])
async def inserisci_risultato(partitaId: str, request: Request):
    """
    Inserisce o aggiorna il risultato di una partita. Aggiorna automaticamente la classifica.
    Body: `{"gol_casa": 2, "gol_ospite": 1}`
    """
    data = await request.json()
    return services.inserisci_risultato(partitaId, data)


# ─────────────────────────────────────────────────────────────────────────────
# CLASSIFICA
# ─────────────────────────────────────────────────────────────────────────────

@app.get(f"{PREFIX}/gironi/{{gironeId}}/classifica", tags=["Classifica"])
async def get_classifica(gironeId: str):
    """Restituisce la classifica di un girone, ordinata per punti."""
    return services.get_classifica(gironeId)
