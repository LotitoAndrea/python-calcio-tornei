// api.js — Modulo centralizzato per tutte le chiamate al backend
const BASE = "/api/v1";

async function _request(method, path, body = null) {
  const opts = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body !== null) opts.body = JSON.stringify(body);

  const res = await fetch(`${BASE}${path}`, opts);
  const data = await res.json();

  if (!res.ok) {
    const msg = data.detail || data.message || JSON.stringify(data);
    throw new Error(msg);
  }
  return data;
}

// ── Tornei ──
export const getTornei = () => _request("GET", "/tornei");
export const getTorneo = (id) => _request("GET", `/tornei/${id}`);
export const creaTorneo = (nome, anno) =>
  _request("POST", "/tornei", { nome, anno });
export const aggiornaTorneo = (id, data) =>
  _request("PATCH", `/tornei/${id}`, data);
export const eliminaTorneo = (id) => _request("DELETE", `/tornei/${id}`);

// ── Squadre ──
export const getSquadre = (torneoId) =>
  _request("GET", `/tornei/${torneoId}/squadre`);
export const creaSquadra = (torneoId, nome) =>
  _request("POST", `/tornei/${torneoId}/squadre`, { nome });

// ── Giocatori ──
export const getGiocatori = (squadraId) =>
  _request("GET", `/squadre/${squadraId}/giocatori`);
export const aggiungiGiocatore = (squadraId, nome, cognome, numero_maglia) =>
  _request("POST", `/squadre/${squadraId}/giocatori`, {
    nome,
    cognome,
    numero_maglia: numero_maglia || null,
  });
export const rimuoviGiocatore = (squadraId, giocatoreId) =>
  _request("DELETE", `/squadre/${squadraId}/giocatori/${giocatoreId}`);

// ── Gironi ──
export const generaGironi = (torneoId, numGironi) =>
  _request("POST", `/tornei/${torneoId}/gironi/genera`, {
    num_gironi: numGironi,
  });
export const getGironi = (torneoId) =>
  _request("GET", `/tornei/${torneoId}/gironi`);

// ── Partite ──
export const generaCalendario = (torneoId) =>
  _request("POST", `/tornei/${torneoId}/partite/genera-calendario`);
export const getPartite = (torneoId) =>
  _request("GET", `/tornei/${torneoId}/partite`);
export const inserisciRisultato = (partitaId, golCasa, golOspite) =>
  _request("POST", `/partite/${partitaId}/risultato`, {
    gol_casa: golCasa,
    gol_ospite: golOspite,
  });

// ── Classifica ──
export const getClassifica = (gironeId) =>
  _request("GET", `/gironi/${gironeId}/classifica`);

// ── Admin ──
export const resetDatabase = () => _request("DELETE", "/reset-db");
