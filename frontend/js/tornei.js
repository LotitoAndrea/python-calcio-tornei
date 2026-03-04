// tornei.js — Logica per index.html (lista tornei)
import { getTornei, creaTorneo, eliminaTorneo } from "./api.js";
import { badgeStato, mostraSuccesso, mostraErrore } from "./utils.js";

const listaEl = document.getElementById("lista-tornei");
const form = document.getElementById("form-crea-torneo");
const inputNome = document.getElementById("input-nome");
const inputAnno = document.getElementById("input-anno");

// ── Carica e renderizza i tornei ──
async function caricaTornei() {
  listaEl.innerHTML = `
    <div class="loading-spinner">
      <div class="spinner-border text-success" role="status">
        <span class="visually-hidden">Caricamento...</span>
      </div>
    </div>`;
  try {
    const tornei = await getTornei();
    if (tornei.length === 0) {
      listaEl.innerHTML = `
        <div class="empty-state">
          <i class="bi bi-trophy"></i>
          <p>Nessun torneo creato. Inizia creandone uno!</p>
        </div>`;
      return;
    }
    listaEl.innerHTML = "";
    const row = document.createElement("div");
    row.className = "row g-3";
    tornei.forEach((t) => {
      const col = document.createElement("div");
      col.className = "col-md-6 col-lg-4";
      col.innerHTML = `
        <div class="card card-torneo stato-${t.stato}">
          <div class="card-body">
            <h6 class="card-title mb-1">${t.nome}</h6>
            <p class="card-text text-muted mb-2">
              <small>Anno ${t.anno} &middot; ${badgeStato(t.stato)}</small>
            </p>
            <div class="d-flex gap-2">
              <a href="torneo.html?id=${t.id}" class="btn btn-sm btn-outline-calcio flex-fill">
                <i class="bi bi-box-arrow-in-right"></i> Apri
              </a>
              <button class="btn btn-sm btn-outline-danger btn-elimina" data-id="${t.id}" data-nome="${t.nome}">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>
        </div>`;
      row.appendChild(col);
    });
    listaEl.appendChild(row);

    // Delegazione eventi per eliminazione
    row.querySelectorAll(".btn-elimina").forEach((btn) => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        const nome = btn.dataset.nome;
        if (!confirm(`Eliminare il torneo "${nome}"?`)) return;
        try {
          await eliminaTorneo(id);
          mostraSuccesso(`Torneo "${nome}" eliminato.`);
          caricaTornei();
        } catch (err) {
          mostraErrore(err.message);
        }
      });
    });
  } catch (err) {
    listaEl.innerHTML = `<div class="alert alert-danger">${err.message}</div>`;
  }
}

// ── Creazione torneo ──
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const nome = inputNome.value.trim();
  const anno = parseInt(inputAnno.value, 10);
  if (!nome) {
    mostraErrore("Il nome del torneo è obbligatorio.");
    return;
  }
  try {
    const t = await creaTorneo(nome, anno);
    mostraSuccesso(`Torneo "${t.nome}" creato con successo!`);
    inputNome.value = "";
    caricaTornei();
  } catch (err) {
    mostraErrore(err.message);
  }
});

// ── Init ──
caricaTornei();
