// utils.js — Funzioni condivise per il frontend

/**
 * Legge un parametro dalla query string.
 */
export function getParametro(nome) {
  return new URLSearchParams(window.location.search).get(nome);
}

/**
 * Restituisce l'HTML di un badge colorato per lo stato del torneo.
 */
export function badgeStato(stato) {
  const map = {
    aperto: "bg-success",
    in_corso: "bg-warning text-dark",
    terminato: "bg-secondary",
  };
  const cls = map[stato] || "bg-info";
  const label = stato.replace("_", " ");
  return `<span class="badge ${cls}">${label}</span>`;
}

// ── Toast Bootstrap ──
let _toastContainer = null;

function _getContainer() {
  if (_toastContainer) return _toastContainer;
  _toastContainer = document.getElementById("toast-container");
  if (!_toastContainer) {
    _toastContainer = document.createElement("div");
    _toastContainer.id = "toast-container";
    _toastContainer.className =
      "toast-container position-fixed bottom-0 end-0 p-3";
    _toastContainer.style.zIndex = "1090";
    document.body.appendChild(_toastContainer);
  }
  return _toastContainer;
}

function _showToast(message, bgClass) {
  const container = _getContainer();
  const id = "toast-" + Date.now();
  const html = `
    <div id="${id}" class="toast align-items-center text-white ${bgClass} border-0" role="alert">
      <div class="d-flex">
        <div class="toast-body">${message}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
      </div>
    </div>`;
  container.insertAdjacentHTML("beforeend", html);
  const el = document.getElementById(id);
  const toast = new bootstrap.Toast(el, { delay: 4000 });
  toast.show();
  el.addEventListener("hidden.bs.toast", () => el.remove());
}

export function mostraSuccesso(msg) {
  _showToast(msg, "bg-success");
}

export function mostraErrore(msg) {
  _showToast(msg, "bg-danger");
}

export function mostraInfo(msg) {
  _showToast(msg, "bg-info");
}

/**
 * Imposta il titolo della pagina e il breadcrumb, se presente.
 */
export function setTitolo(titolo) {
  document.title = `${titolo} — Tornei Calcistici`;
}

/**
 * Helper per creare elementi HTML velocemente.
 */
export function el(tag, attrs = {}, ...children) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "className") e.className = v;
    else if (k === "innerHTML") e.innerHTML = v;
    else if (k.startsWith("on")) e.addEventListener(k.slice(2).toLowerCase(), v);
    else e.setAttribute(k, v);
  }
  for (const c of children) {
    if (typeof c === "string") e.appendChild(document.createTextNode(c));
    else if (c) e.appendChild(c);
  }
  return e;
}
