🎯 Esercizio 2: Modello di Dominio e Persistenza Dati (CRUD)

Questo modulo si concentra sull'integrazione di un modello di business (la classe Prodotto) con un sistema di persistenza esterno (PostgreSQL), completando tutte le operazioni necessarie per la gestione del ciclo di vita di un dato.

🛠️ Contenuti e Competenze

1. Modello di Dominio (classe.py)

Il file classe.py definisce la logica di business fondamentale del progetto:

    Classe Prodotto: Implementazione completa con incapsulamento (Getter e Setter).

    Precisione Finanziaria: Uso del modulo decimal per garantire la precisione nei calcoli di prezzo.

    Logica del Lordo: Calcolo automatico e corretto del prezzo Lordo in base all'aliquota IVA.

    Validazione: Uso dei setter e Exception Handling per prevenire l'inserimento di dati non validi (es. prezzi negativi).

2. Strato di Persistenza (db_manager.py)

La classe ProdottoDBManager gestisce la comunicazione sicura e transazionale con il database PostgreSQL.

    Sicurezza: Le credenziali del database sono gestite tramite il file .env e caricate con python-dotenv, evitando l'hardcoding.

    Connessione Sicura: I metodi connetti() e disconnetti() garantiscono una gestione sicura delle risorse.

    Operazioni CRUD Complete:

        Create (inserisci_prodotto): Utilizza COMMIT e ROLLBACK per transazioni atomiche.

        Read (leggi_prodotti): Esegue SELECT e ricostruisce gli oggetti Prodotto Python.

        Update (aggiorna_prodotto): Modifica i dati del prodotto nel DB in base al codice.

        Delete (elimina_prodotto): Rimuove il record e gestisce il rowcount per la verifica.

⚙️ Istruzioni per l'Esecuzione

Per eseguire i test CRUD presenti nel blocco if __name__ == '__main__': di db_manager.py:

    Assicurati che l'ambiente virtuale sia attivo e che PostgreSQL sia in esecuzione.

    Esegui il modulo dal terminale:
    Bash

    python -m esercizio2.db_manager

