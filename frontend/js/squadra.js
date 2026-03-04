// squadra.js — Logica per squadra.html (dettaglio squadra e giocatori)
import {
  getSquadre,
  getTorneo,
  getGiocatori,
  aggiungiGiocatore,
  rimuoviGiocatore,
} from "./api.js";
import {
  getParametro,
  mostraSuccesso,
  mostraErrore,
} from "./utils.js";

const squadraId = getParametro("id");
const torneoId = getParametro("torneo");

if (!squadraId || !torneoId) {
  window.location.href = "index.html";
}

// DOM refs
const nomeSquadraEl = document.getElementById("nome-squadra");
const infoSquadraEl = document.getElementById("info-squadra");
const bcTorneoLink = document.getElementById("bc-torneo-link");
const bcSquadra = document.getElementById("bc-squadra");
const btnTornaTorneo = document.getElementById("btn-torna-torneo");
const formGiocatore = document.getElementById("form-giocatore");
const inputNome = document.getElementById("input-g-nome");
const inputCognome = document.getElementById("input-g-cognome");
const inputMaglia = document.getElementById("input-g-maglia");
const listaGiocatoriEl = document.getElementById("lista-giocatori");

// Link ritorno al torneo
bcTorneoLink.href = `torneo.html?id=${torneoId}`;
btnTornaTorneo.href = `torneo.html?id=${torneoId}`;

// ── Carica dati ──
async function caricaDati() {
  try {
    const [torneo, squadre, giocatori] = await Promise.all([
      getTorneo(torneoId),
      getSquadre(torneoId),
      getGiocatori(squadraId),
    ]);

    const squadra = squadre.find((s) => s.id === squadraId);
    if (!squadra) {
      mostraErrore("Squadra non trovata.");
      return;
    }

    // Aggiorna intestazioni
    nomeSquadraEl.textContent = squadra.nome;
    bcTorneoLink.textContent = torneo.nome;
    bcSquadra.textContent = squadra.nome;
    document.title = `${squadra.nome} — Tornei Calcistici`;
    infoSquadraEl.innerHTML = `Torneo: <strong>${torneo.nome}</strong> &middot; Giocatori: <strong>${giocatori.length}</strong>`;

    renderGiocatori(giocatori);
  } catch (err) {
    mostraErrore(err.message);
  }
}

function renderGiocatori(giocatori) {
  if (giocatori.length === 0) {
    listaGiocatoriEl.innerHTML = `
      <div class="empty-state">
        <i class="bi bi-person-x"></i>
        <p>Nessun giocatore in rosa. Aggiungine uno!</p>
      </div>`;
    return;
  }

  let html = `<div class="table-responsive"><table class="table table-hover table-sm">
    <thead class="table-light">
      <tr><th>Nome</th><th>Cognome</th><th>N° Maglia</th><th></th></tr>
    </thead><tbody>`;
  giocatori.forEach((g) => {
    html += `<tr>
      <td>${g.nome}</td>
      <td>${g.cognome}</td>
      <td>${g.numero_maglia != null ? g.numero_maglia : "—"}</td>
      <td class="text-end">
        <button class="btn btn-sm btn-outline-danger btn-rimuovi" data-id="${g.id}">
          <i class="bi bi-trash"></i> Rimuovi
        </button>
      </td>
    </tr>`;
  });
  html += `</tbody></table></div>`;
  listaGiocatoriEl.innerHTML = html;

  // Event: rimuovi giocatore
  listaGiocatoriEl.querySelectorAll(".btn-rimuovi").forEach((btn) => {
    btn.addEventListener("click", async () => {
      if (!confirm("Rimuovere questo giocatore?")) return;
      try {
        await rimuoviGiocatore(squadraId, btn.dataset.id);
        mostraSuccesso("Giocatore rimosso.");
        caricaDati();
      } catch (err) {
        mostraErrore(err.message);
      }
    });
  });
}

// ── Aggiungi giocatore ──
formGiocatore.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = inputNome.value.trim();
  const cognome = inputCognome.value.trim();
  const maglia = inputMaglia.value ? parseInt(inputMaglia.value, 10) : null;
  if (!nome || !cognome) return;
  try {
    const g = await aggiungiGiocatore(squadraId, nome, cognome, maglia);
    mostraSuccesso(`${g.nome} ${g.cognome} aggiunto alla rosa!`);
    inputNome.value = "";
    inputCognome.value = "";
    inputMaglia.value = "";
    caricaDati();
  } catch (err) {
    mostraErrore(err.message);
  }
});

// ── Init ──
caricaDati();
