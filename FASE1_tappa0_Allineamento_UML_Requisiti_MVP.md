# Allineamento UML → Requisiti Tecnici (Fase 1 – Tappa 0)
Progetto: **Sistema di Gestione Tornei Scolastici (SGTS)** – *focus: tornei di calcio*  
Gruppo: Lotito Andrea, Mirabelli Gabriel, Jack Nwankwo, Riccardo Aldo Gianotti

> Base requisiti: Documento “SGTS” (versione concettuale). fileciteturn1file0

---

## 1) Entità principali (dal diagramma UML)

### Torneo
Attributi principali: `idTorneo`, `nome`, `anniScolastici`, `sport`, `giocatoriInCampo`, `minAnnoNascita`, `maxAnnoNascita`, `dataInizio`, `dataFine`.

### Fase
Attributi principali: `idFase`, `nomeFase`, `tipo` (es. *GIRONI* / *ELIMINAZIONE*), `ordine`.

### Girone
Attributi principali: `idGirone`, `codiceGirone`, `numeroSquadre`.

### Squadra
Attributi principali: `idSquadra`, `nomeSquadra`, `classe`, `sezione`.

### Giocatore
Attributi principali: `idGiocatore`, `nome`, `cognome`, `annoNascita`, `ruolo`.

### Partita
Attributi principali: `idPartita`, `dataOra`, `campo`, `goalCasa`, `goalOspite`, `squadraCasa`, `squadraOspite`, `esito`.

### Risultato (concetto)
Nel modello è rappresentato dai campi di **Partita**: `goalCasa`, `goalOspite`, `esito` (eventuali rigori/extra-time sono estensioni future).

### IscrizioneGirone (associativa)
Attributi principali: `punti`, `goalFatti`, `goalSubiti`, `differenzaReti` (derivabile), `posizioneFinaleGirone`.

---

## 2) Relazioni e cardinalità (dal diagramma UML + allineamento tecnico)

- **Torneo (1) — (0..N) Squadra**  
  Un torneo può avere molte squadre; ogni squadra appartiene a un solo torneo.

- **Torneo (1) — (1..N) Fase**  
  Un torneo è composto da almeno una fase.

- **Fase (0..1) — (1..N) Girone**  
  Solo le fasi di tipo *GIRONI* hanno gironi; una fase può avere molti gironi.

- **Fase (1) — (0..N) Partita**  
  Una fase può non avere ancora partite generate; ogni partita appartiene a una fase.

- **Squadra (1) — (1..N) Giocatore**  
  Una squadra è composta da uno o più giocatori; ogni giocatore appartiene a una squadra.

- **Girone (1) — (1..N) IscrizioneGirone — (1) Squadra**  
  L’iscrizione collega squadre e gironi con dati di classifica.  
  **Nota di allineamento tecnico:** IscrizioneGirone deve referenziare **sia** `idGirone` **sia** `idSquadra` (chiave composta o vincolo di unicità su coppia).

- **Partita — Squadra (Casa/Ospite)**  
  Ogni partita deve avere **1** squadra casa e **1** squadra ospite; una squadra può giocare **0..N** partite.  
  **Regola:** `squadraCasa != squadraOspite`.

- **Allineamento necessario per le classifiche gironi (RF4):**  
  Le partite della fase a gironi devono essere associabili a un **Girone** (es. `idGirone` opzionale in Partita, valorizzato solo in fase *GIRONI*).

---

## 3) Requisiti funzionali tecnici (10–15) – “Il sistema deve…”

1. Il sistema deve permettere la creazione di un **torneo** con i campi minimi: nome, anno scolastico, sport, giocatori in campo, min/max anno di nascita, data inizio/fine. fileciteturn1file0
2. Il sistema deve permettere di aggiungere, modificare e visualizzare le **squadre** associate a un torneo (nomeSquadra, classe, sezione).
3. Il sistema deve permettere di aggiungere, modificare e visualizzare i **giocatori** associati a una squadra (nome, cognome, annoNascita, ruolo).
4. Il sistema deve validare che `annoNascita` del giocatore rientri nei limiti del torneo (`minAnnoNascita`–`maxAnnoNascita`).
5. Il sistema deve permettere di definire le **fasi** di un torneo (nomeFase, tipo, ordine) e di elencarle in ordine crescente.
6. Il sistema deve generare automaticamente i **gironi** per una fase di tipo *GIRONI*, distribuendo le squadre in gruppi da 3 a 6. fileciteturn1file0
7. Il sistema deve creare le **iscrizioni ai gironi** (IscrizioneGirone) collegando ogni squadra al proprio girone e inizializzando punti/goal a 0.
8. Il sistema deve generare automaticamente il **calendario partite** della fase a gironi, garantendo che ogni squadra affronti le altre del proprio girone almeno una volta (round-robin).
9. Il sistema deve permettere di inserire/modificare il **risultato** di una partita (goalCasa, goalOspite) e calcolare l’**esito** (casa/ospite/pareggio).
10. Il sistema deve aggiornare la **classifica del girone** in base ai risultati inseriti (punti, goalFatti, goalSubiti, differenzaReti). fileciteturn1file0
11. Il sistema deve applicare i criteri di parità (ordine: punti, differenza reti, goal fatti, scontro diretto se disponibile) per determinare la posizione nel girone.
12. Il sistema deve calcolare le **qualificate** dai gironi (es. prime 2) e generare la fase finale a eliminazione diretta. fileciteturn1file0
13. Il sistema deve gestire numeri di qualificate non potenza di 2 attraverso una fase preliminare (spareggi) o byes configurabili. fileciteturn1file0
14. Il sistema deve generare un **report** del torneo (regolamento/calendario/classifiche/report finale) esportabile almeno in formato Word; PDF come estensione. fileciteturn1file0
15. Il sistema deve permettere la consultazione pubblica (sola lettura) di calendario, risultati e classifiche di un torneo.

---

## 4) MVP minimo (Backend “fatto”)

Il backend è considerato completato (MVP) quando sono disponibili e funzionanti:

- CRUD base: **Torneo**, **Squadra**, **Giocatore**
- Creazione **Fase** e generazione **Gironi** (con iscrizioni)
- Generazione **partite di girone** (calendario)
- Inserimento **risultati** e calcolo **classifiche** per girone
- Endpoint di consultazione: tornei, squadre, partite, classifiche
- Export **Word** del riepilogo torneo (almeno calendario + classifiche)

---

## 5) Output di consegna
Questo documento può essere consegnato come **MD** o convertito in **PDF**.
