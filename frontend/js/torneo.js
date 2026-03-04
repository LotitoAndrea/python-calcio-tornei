// torneo.js — Logica per torneo.html (dettaglio torneo)
import {
  getTorneo,
  aggiornaTorneo,
  getSquadre,
  creaSquadra,
  getGironi,
  generaGironi,
  getPartite,
  generaCalendario,
  inserisciRisultato,
  getClassifica,
} from "./api.js";
import {
  getParametro,
  badgeStato,
  mostraSuccesso,
  mostraErrore,
} from "./utils.js";

const torneoId = getParametro("id");
if (!torneoId) {
  window.location.href = "index.html";
}

// ── DOM refs ──
const infoEl = document.getElementById("info-torneo");
const bcTorneo = document.getElementById("bc-torneo");
const formSquadra = document.getElementById("form-aggiungi-squadra");
const inputSquadraNome = document.getElementById("input-squadra-nome");
const listaSquadreEl = document.getElementById("lista-squadre");
const formGironi = document.getElementById("form-genera-gironi");
const inputNumGironi = document.getElementById("input-num-gironi");
const listaGironiEl = document.getElementById("lista-gironi");
const btnGeneraCalendario = document.getElementById("btn-genera-calendario");
const listaPartiteEl = document.getElementById("lista-partite");
const selectGirone = document.getElementById("select-girone-classifica");
const classificaEl = document.getElementById("classifica-container");

// ═══════════════════════════════════════════════════════════════
// INFO TORNEO
// ═══════════════════════════════════════════════════════════════
async function caricaInfo() {
  try {
    const t = await getTorneo(torneoId);
    bcTorneo.textContent = t.nome;
    document.title = `${t.nome} — Tornei Calcistici`;
    infoEl.innerHTML = `
      <div class="row align-items-center">
        <div class="col-md-6">
          <h4 class="mb-1">${t.nome}</h4>
          <p class="text-muted mb-0">Anno ${t.anno} &middot; ${badgeStato(t.stato)}</p>
        </div>
        <div class="col-md-6 text-md-end mt-3 mt-md-0">
          <div class="btn-group" role="group">
            <button class="btn btn-sm ${t.stato === "aperto" ? "btn-success" : "btn-outline-success"}" data-stato="aperto">Aperto</button>
            <button class="btn btn-sm ${t.stato === "in_corso" ? "btn-warning" : "btn-outline-warning"}" data-stato="in_corso">In Corso</button>
            <button class="btn btn-sm ${t.stato === "terminato" ? "btn-secondary" : "btn-outline-secondary"}" data-stato="terminato">Terminato</button>
          </div>
        </div>
      </div>`;
    // Cambio stato
    infoEl.querySelectorAll("[data-stato]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        try {
          await aggiornaTorneo(torneoId, { stato: btn.dataset.stato });
          mostraSuccesso(`Stato aggiornato a "${btn.dataset.stato}".`);
          caricaInfo();
        } catch (err) {
          mostraErrore(err.message);
        }
      });
    });
  } catch (err) {
    infoEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

// ═══════════════════════════════════════════════════════════════
// SQUADRE
// ═══════════════════════════════════════════════════════════════
async function caricaSquadre() {
  try {
    const squadre = await getSquadre(torneoId);
    if (squadre.length === 0) {
      listaSquadreEl.innerHTML = `<p class="text-muted">Nessuna squadra ancora. Aggiungine una!</p>`;
      return;
    }
    let html = `<div class="table-responsive"><table class="table table-hover table-sm mb-0">
      <thead class="table-light"><tr><th>Nome</th><th>Giocatori</th><th></th></tr></thead><tbody>`;
    squadre.forEach((s) => {
      html += `<tr>
        <td><strong>${s.nome}</strong></td>
        <td><span class="badge bg-secondary">${s.giocatori.length}</span></td>
        <td class="text-end">
          <a href="squadra.html?id=${s.id}&torneo=${torneoId}" class="btn btn-sm btn-outline-calcio">
            <i class="bi bi-eye"></i> Dettagli
          </a>
        </td>
      </tr>`;
    });
    html += `</tbody></table></div>`;
    listaSquadreEl.innerHTML = html;
  } catch (err) {
    listaSquadreEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

formSquadra.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = inputSquadraNome.value.trim();
  if (!nome) return;
  try {
    await creaSquadra(torneoId, nome);
    mostraSuccesso(`Squadra "${nome}" aggiunta!`);
    inputSquadraNome.value = "";
    caricaSquadre();
  } catch (err) {
    mostraErrore(err.message);
  }
});

// ═══════════════════════════════════════════════════════════════
// GIRONI
// ═══════════════════════════════════════════════════════════════
let gironiCache = [];

async function caricaGironi() {
  try {
    const gironi = await getGironi(torneoId);
    gironiCache = gironi;
    aggiornaSelectGironi(gironi);
    if (gironi.length === 0) {
      listaGironiEl.innerHTML = `<p class="text-muted">Nessun girone generato.</p>`;
      return;
    }
    // Carica le squadre per mostrare i nomi
    const squadre = await getSquadre(torneoId);
    const mapSquadre = {};
    squadre.forEach((s) => (mapSquadre[s.id] = s.nome));

    let html = `<div class="row g-3">`;
    gironi.forEach((g) => {
      html += `
        <div class="col-md-6 col-lg-4">
          <div class="card girone-card">
            <div class="card-body">
              <h6 class="card-title"><i class="bi bi-diagram-3"></i> ${g.nome}</h6>
              <ul class="list-group list-group-flush">`;
      g.squadre.forEach((sid) => {
        html += `<li class="list-group-item py-1"><i class="bi bi-shield-fill"></i> ${mapSquadre[sid] || sid}</li>`;
      });
      html += `</ul></div></div></div>`;
    });
    html += `</div>`;
    listaGironiEl.innerHTML = html;
  } catch (err) {
    listaGironiEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

function aggiornaSelectGironi(gironi) {
  selectGirone.innerHTML = `<option value="">— scegli un girone —</option>`;
  gironi.forEach((g) => {
    selectGirone.innerHTML += `<option value="${g.id}">${g.nome}</option>`;
  });
}

formGironi.addEventListener("submit", async (e) => {
  e.preventDefault();
  const num = parseInt(inputNumGironi.value, 10);
  try {
    await generaGironi(torneoId, num);
    mostraSuccesso("Gironi generati con successo!");
    caricaGironi();
    caricaPartite();
  } catch (err) {
    mostraErrore(err.message);
  }
});

// ═══════════════════════════════════════════════════════════════
// PARTITE
// ═══════════════════════════════════════════════════════════════
async function caricaPartite() {
  try {
    const partite = await getPartite(torneoId);
    if (partite.length === 0) {
      listaPartiteEl.innerHTML = `<p class="text-muted">Nessuna partita. Genera prima i gironi, poi il calendario.</p>`;
      return;
    }

    // Raggruppa per girone
    const perGirone = {};
    partite.forEach((p) => {
      const key = p.girone_nome || p.girone_id;
      if (!perGirone[key]) perGirone[key] = [];
      perGirone[key].push(p);
    });

    let html = "";
    for (const [girone, partiteGirone] of Object.entries(perGirone)) {
      html += `<h6 class="mt-3 mb-2"><i class="bi bi-diagram-3"></i> ${girone}</h6>`;
      partiteGirone.forEach((p) => {
        const giocata = p.giocata;
        html += `
          <div class="partita-card ${giocata ? "giocata" : ""}">
            <span class="team-name text-end" style="flex:1">${p.squadra_casa_nome}</span>
            ${
              giocata
                ? `<span class="score">${p.gol_casa} - ${p.gol_ospite}</span>`
                : `<span class="vs">VS</span>`
            }
            <span class="team-name" style="flex:1">${p.squadra_ospite_nome}</span>
            ${
              !giocata
                ? `<form class="d-flex gap-1 align-items-center form-risultato" data-id="${p.id}">
                    <input type="number" class="form-control form-control-sm" min="0" style="width:55px" placeholder="C" required />
                    <span>-</span>
                    <input type="number" class="form-control form-control-sm" min="0" style="width:55px" placeholder="O" required />
                    <button type="submit" class="btn btn-sm btn-calcio"><i class="bi bi-check-lg"></i></button>
                  </form>`
                : `<button class="btn btn-sm btn-outline-secondary btn-modifica-risultato" 
                      data-id="${p.id}" data-casa="${p.gol_casa}" data-ospite="${p.gol_ospite}">
                    <i class="bi bi-pencil"></i>
                  </button>`
            }
          </div>`;
      });
    }
    listaPartiteEl.innerHTML = html;

    // Event: inserisci risultato
    listaPartiteEl.querySelectorAll(".form-risultato").forEach((form) => {
      form.addEventListener("submit", async (ev) => {
        ev.preventDefault();
        const inputs = form.querySelectorAll("input");
        const golC = parseInt(inputs[0].value, 10);
        const golO = parseInt(inputs[1].value, 10);
        try {
          await inserisciRisultato(form.dataset.id, golC, golO);
          mostraSuccesso("Risultato salvato!");
          caricaPartite();
          // ricarica classifica se un girone è selezionato
          if (selectGirone.value) caricaClassifica(selectGirone.value);
        } catch (err) {
          mostraErrore(err.message);
        }
      });
    });

    // Event: modifica risultato
    listaPartiteEl.querySelectorAll(".btn-modifica-risultato").forEach((btn) => {
      btn.addEventListener("click", () => {
        const card = btn.closest(".partita-card");
        const scoreSpan = card.querySelector(".score");
        const id = btn.dataset.id;
        const casa = btn.dataset.casa;
        const ospite = btn.dataset.ospite;
        scoreSpan.outerHTML = `
          <form class="d-flex gap-1 align-items-center form-risultato" data-id="${id}">
            <input type="number" class="form-control form-control-sm" min="0" style="width:55px" value="${casa}" required />
            <span>-</span>
            <input type="number" class="form-control form-control-sm" min="0" style="width:55px" value="${ospite}" required />
            <button type="submit" class="btn btn-sm btn-calcio"><i class="bi bi-check-lg"></i></button>
          </form>`;
        btn.remove();
        const newForm = card.querySelector(".form-risultato");
        newForm.addEventListener("submit", async (ev) => {
          ev.preventDefault();
          const inputs = newForm.querySelectorAll("input");
          const golC = parseInt(inputs[0].value, 10);
          const golO = parseInt(inputs[1].value, 10);
          try {
            await inserisciRisultato(id, golC, golO);
            mostraSuccesso("Risultato aggiornato!");
            caricaPartite();
            if (selectGirone.value) caricaClassifica(selectGirone.value);
          } catch (err) {
            mostraErrore(err.message);
          }
        });
      });
    });
  } catch (err) {
    listaPartiteEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

btnGeneraCalendario.addEventListener("click", async () => {
  try {
    await generaCalendario(torneoId);
    mostraSuccesso("Calendario generato!");
    caricaPartite();
  } catch (err) {
    mostraErrore(err.message);
  }
});

// ═══════════════════════════════════════════════════════════════
// CLASSIFICA
// ═══════════════════════════════════════════════════════════════
async function caricaClassifica(gironeId) {
  if (!gironeId) {
    classificaEl.innerHTML = "";
    return;
  }
  try {
    const rows = await getClassifica(gironeId);
    if (rows.length === 0) {
      classificaEl.innerHTML = `<p class="text-muted">Nessun dato disponibile per questo girone.</p>`;
      return;
    }
    let html = `
      <div class="table-responsive">
        <table class="table table-sm table-classifica mb-0">
          <thead>
            <tr>
              <th>#</th><th>Squadra</th><th>Pts</th><th>G</th>
              <th>V</th><th>P</th><th>S</th><th>GF</th><th>GS</th><th>DR</th>
            </tr>
          </thead>
          <tbody>`;
    rows.forEach((r) => {
      html += `<tr>
        <td>${r.posizione}</td>
        <td><strong>${r.squadra_nome}</strong></td>
        <td><strong>${r.punti}</strong></td>
        <td>${r.partite_giocate}</td>
        <td>${r.vittorie}</td>
        <td>${r.pareggi}</td>
        <td>${r.sconfitte}</td>
        <td>${r.gol_fatti}</td>
        <td>${r.gol_subiti}</td>
        <td>${r.differenza_reti > 0 ? "+" : ""}${r.differenza_reti}</td>
      </tr>`;
    });
    html += `</tbody></table></div>`;
    classificaEl.innerHTML = html;
  } catch (err) {
    classificaEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

selectGirone.addEventListener("change", () => {
  caricaClassifica(selectGirone.value);
});

// ═══════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════
async function init() {
  await caricaInfo();
  await caricaSquadre();
  await caricaGironi();
  await caricaPartite();
}
init();
