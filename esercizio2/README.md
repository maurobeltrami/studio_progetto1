# 🚀 Esercizio 2: Mini-ERP con Persistenza PostgreSQL e Relazioni

Questo progetto è parte del modulo **"MESE 1: FONDAMENTI ACCELERATI (Python per ERP e SQL)"** del Piano di Studio per Programmatore Freelance Odoo.

## 🎯 Obiettivo Raggiunto

L'obiettivo di questo esercizio era sviluppare una solida base tecnica per la gestione dei dati, simulando le funzionalità CRUD fondamentali di un sistema ERP, in preparazione all'uso dell'ORM di Odoo.

**Stato Attuale: Completato (CRUD + Many2one)**

## ⚙️ Funzionalità Implementate (CRUD)

Il modulo `db_manager.py` implementa tutte le operazioni essenziali su una singola entità (`Prodotto`), gestendo la comunicazione sicura con un database PostgreSQL.

1.  **Create (Inserimento):** Inserimento di nuove istanze di `Prodotto` nel database.
2.  **Read (Lettura):**
    * Lettura di tutti i prodotti attivi.
    * Ricerca per codice esatto.
    * Ricerca avanzata con filtri multipli (nome, prezzo massimo).
3.  **Update (Aggiornamento):** Modifica dei dati di un prodotto esistente.
4.  **Delete (Eliminazione Logica):** L'eliminazione è simulata (soft-delete), mantenendo il record ma marcandolo come non attivo.

## 🔗 Relazione Essenziale Implementata: Many2one (Prodotto -> Fornitore)

In linea con l'architettura dei sistemi ERP come Odoo, è stata implementata la prima relazione tra modelli:

* **Entità:** `Prodotto` (Many) e `Fornitore` (One).
* **Logica:** Ogni Prodotto può avere un solo Fornitore principale.
* **Tecnologia:** La relazione è gestita nel database tramite una **Chiave Esterna** (`id_fornitore`) e nel codice Python tramite una `LEFT JOIN` e l'istanziamento di due oggetti correlati (`Prodotto` contiene un riferimento a `Fornitore`).

## 💻 Istruzioni per l'Avvio

1.  **Configurazione Database:**
    * Assicurarsi che il server PostgreSQL sia attivo.
    * Avere un database chiamato `studio_progetto_erp` (o quello configurato nel file `.env`).
    * Eseguire i comandi SQL per creare le tabelle `prodotti` e `fornitori` e impostare la chiave esterna (se non è stato già fatto):
        ```sql
        CREATE TABLE fornitori (id SERIAL PRIMARY KEY, nome VARCHAR(100) NOT NULL UNIQUE);
        -- Esegui gli aggiornamenti per la tabella prodotti se stai usando un database esistente.
        ```

2.  **Esecuzione:**
    * Assicurarsi di essere all'interno dell'ambiente virtuale.
    * Eseguire il modulo principale dalla cartella `esercizi/esercizio2/`:
        ```bash
        python -m esercizio2.main
        ```

3.  **Interazione:**
    * Utilizzare il menu CLI per interagire (inserimento, visualizzazione, ricerca) e testare la persistenza e la corretta visualizzazione della relazione Fornitore (opzioni 1, 2 e 7).

## ⏭️ Prossimi Passi

Il prossimo obiettivo del piano di studi è sfruttare questa logica di business in un contesto web, creando una **API RESTful** con **Flask** per mappare le operazioni CRUD ai metodi HTTP (GET, POST, PUT, DELETE).
