🐍 Corso di Sviluppo Software in Python (Focus: Backend e Database)

Questo repository contiene il codice sviluppato durante un corso pratico e intensivo di sviluppo software in Python. Il percorso è progettato per coprire le basi del linguaggio, la gestione dei file, la Programmazione Orientata agli Oggetti (OOP) e l'integrazione di un'applicazione con un database relazionale PostgreSQL.

Obiettivi di Competenza Raggiunti

Il corso mira a consolidare le seguenti competenze fondamentali per lo sviluppo backend:

    OOP & Modelli di Dominio: Creazione di classi modulari (Prodotto), incapsulamento e validazione dei dati.

    Gestione dei Dati (CRUD): Implementazione completa delle quattro operazioni di base (Create, Read, Update, Delete) su PostgreSQL.

    Persistenza Dati: Utilizzo del driver psycopg2 per la comunicazione con PostgreSQL.

    Sicurezza: Implementazione dell'uso di variabili d'ambiente (python-dotenv) per non esporre le credenziali del database nel codice sorgente.

    File Handling: Capacità di leggere e scrivere dati in formato CSV (Esercizio 1).

📂 Struttura del Corso

Il corso è suddiviso in moduli pratici, ciascuno con i propri obiettivi e directory:
Modulo	Obiettivo Principale	Status
Esercizio 1	Calcolo IVA e Output CSV (Introduzione al File Handling)	COMPLETATO
Esercizio 2	OOP Avanzata, Database (PostgreSQL) e Ciclo CRUD	COMPLETATO
Esercizio 3	Integrazione API/Web (futuro)	In Sviluppo

⚙️ Configurazione per l'Esecuzione

Per poter eseguire e replicare gli esercizi, è necessario:

    Avere un'istanza di PostgreSQL in esecuzione.

    Creare un ambiente virtuale (es. python3 -m venv venv) e attivarlo.

    Installare le dipendenze: pip install psycopg2-binary python-dotenv.

    Creare un file .env nella cartella radice con le credenziali del database.