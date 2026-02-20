# store.py - Archivio dati in memoria (dizionari Python)
# Nessun database, nessun ORM: solo strutture native Python.

from typing import Any

# Tutti i dati vengono persi al riavvio del server (soluzione scolastica).

tornei: dict[str, Any] = {}
squadre: dict[str, Any] = {}
giocatori: dict[str, Any] = {}
gironi: dict[str, Any] = {}
partite: dict[str, Any] = {}
classifiche: dict[str, Any] = {}   # chiave: "{gironeId}_{squadraId}"
