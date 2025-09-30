## 📦 Esercizio 2: Classe Prodotto e Operazioni CRUD

Questo esercizio approfondisce i concetti di **Programmazione Orientata agli Oggetti (OOP)**, essenziali per la modellazione dei dati nei sistemi ERP come Odoo.

### 🎯 Obiettivo del Progetto

Implementare una Classe `Prodotto` e i suoi metodi per simulare le quattro operazioni fondamentali sul ciclo di vita di un dato in memoria:
* **C**reate (usando `__init__`)
* **R**ead (usando `__str__`)
* **U**pdate (usando `aggiorna_prezzo`)
* **D**elete (usando la funzione `del`)

### 🛡️ Gestione delle Eccezioni (Exception Handling)

La Classe `Prodotto` è stata rafforzata per garantire l'integrità dei dati, un requisito fondamentale per i sistemi ERP.

* **Validazione in `__init__`:** Il costruttore ora chiama un metodo `_valida_dati()` che solleva un'eccezione **`ValueError`** se:
    1.  Il `codice` o il `nome` del prodotto sono vuoti.
    2.  Il `prezzo_netto` o l'`aliquota_iva` sono valori negativi.
* **Gestione Esterna:** Il blocco `try...except ValueError` è utilizzato nel codice di test per catturare gli errori di validazione e permettere al programma di continuare a funzionare senza bloccarsi.

### 📁 Struttura del Codice

Il codice principale si trova nel file: `esercizio_02/classe.py`

### ⚙️ Dettagli Tecnici

* **Librerie:** Nessuna libreria esterna richiesta (solo Python Core).
* **Concetti chiave:** Attributi di istanza (`self.nome`), metodi (`calcola_prezzo_lordo`), metodi speciali (`__init__`, `__str__`).
