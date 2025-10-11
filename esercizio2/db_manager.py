import psycopg2
# Importazioni per la sicurezza e la gestione dei moduli
import os
from dotenv import load_dotenv
from .classe import Prodotto 

# Carica le variabili d'ambiente dal file .env (deve essere nella cartella radice)
load_dotenv() 

# Configurazione del database: legge le credenziali da .env
# Usiamo os.environ.get('VAR', 'DEFAULT') per sicurezza, in caso la variabile non sia impostata
DB_CONFIG = {
    "host": "localhost",
    "database": os.environ.get("DB_NAME", "studio_progetto_erp"),
    "user": os.environ.get("DB_USER", "mauroi"),
    "password": os.environ.get("DB_PASSWORD", "la_tua_password_segreta")
}

class ProdottoDBManager:
    """
    Gestisce la connessione e le operazioni CRUD per la tabella prodotti.
    """
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connetti(self):
        """Stabilisce una connessione al database, gestendo le eccezioni."""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✅ Connessione a PostgreSQL riuscita.")
            return True
        except psycopg2.Error as e:
            print(f"❌ Errore durante la connessione a PostgreSQL: {e}")
            return False

    def disconnetti(self):
        """Chiude la connessione e il cursore in modo sicuro."""
        if self.cursor:
            self.cursor.close()
            
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("✅ Connessione a PostgreSQL chiusa.")

    def inserisci_prodotto(self, prodotto):
        """
        Inserisce un nuovo prodotto nel database usando i dati validati.
        Gestisce la transazione (COMMIT/ROLLBACK).
        """
        
        query = """
        INSERT INTO prodotti (codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id; 
        """
        
        # Tupla dei valori estratti dall'oggetto Prodotto
        valori = (
            prodotto.codice,
            prodotto.nome,
            prodotto.prezzo_netto,
            prodotto.aliquota_iva,
            prodotto.prezzo_lordo
        )
        
        try:
            # Esecuzione della Query
            self.cursor.execute(query, valori)
            
            # Recupero dell'ID generato
            nuovo_id = self.cursor.fetchone()[0]
            
            # Commit: Rende la modifica permanente
            self.conn.commit()
            
            print(f"✅ Prodotto '{prodotto.nome}' inserito con successo! ID DB: {nuovo_id}")
            
            return nuovo_id
            
        except psycopg2.Error as e:
            # Rollback: Annulla l'operazione in caso di errore (es. codice duplicato)
            if self.conn:
                self.conn.rollback()
            
            print(f"❌ Errore DB durante l'inserimento: {e}")
            return None
        
        except Exception as e:
            # Rollback per errori generici
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return None

    def leggi_prodotti(self):
        """
        Recupera tutti i prodotti attivi dal database e li restituisce come lista di oggetti Prodotto.
        
        Returns:
            list[Prodotto]: Una lista di istanze di oggetti Prodotto.
        """
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile leggere i dati.")
            return []
            
        # 1. Query SQL per selezionare tutti i campi dalla tabella prodotti
        query = "SELECT codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo FROM prodotti WHERE attivo = TRUE;"
        
        prodotti_letti = []
        
        try:
            # Esecuzione della Query
            self.cursor.execute(query)
            
            # 2. Recupero di tutti i risultati
            risultati = self.cursor.fetchall()
            
            # 3. Iterazione e Ricostruzione degli Oggetti
            for riga in risultati:
                # La riga è una tupla: (codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo)
                codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo = riga
                
                # Ricostruiamo l'oggetto Prodotto usando il costruttore della classe
                # Nota: Passiamo solo i dati che il costruttore ha bisogno per l'inizializzazione
                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome,
                    prezzo_netto=float(prezzo_netto),  # Converte Decimal da DB a float Python
                    aliquota_iva=float(aliquota_iva),
                    # Il prezzo_lordo e attivo non vengono passati al costruttore, ma si calcolano/settano dopo
                )
                # Il database gestisce la verità. Potresti voler sovrascrivere il calcolo del Lordo (o no)
                # In questo caso, lo lasciamo calcolare dalla classe, a meno che non sia necessario importare il valore esatto.
                # Per ora, la ricostruzione è sufficiente.
                
                prodotti_letti.append(prodotto_ricostruito)

            print(f"✅ Lettura completata. Trovati {len(prodotti_letti)} prodotti attivi.")
            return prodotti_letti

        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la lettura dei prodotti: {e}")
            return []
        except Exception as e:
            print(f"❌ Errore generico durante la ricostruzione dei prodotti: {e}")
            return []

    # ... (all'interno della classe ProdottoDBManager, dopo leggi_prodotti)

    def leggi_prodotto_per_codice(self, codice):
        """
        Recupera un singolo prodotto dal database, identificandolo tramite il codice.
        
        Returns:
            Prodotto or None: L'istanza di Prodotto se trovata, altrimenti None.
        """
        if not self.conn:
            return None
            
        # Query SQL per selezionare tutti i campi di un singolo prodotto
        query = "SELECT codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo FROM prodotti WHERE codice = %s AND attivo = TRUE;"
        
        try:
            self.cursor.execute(query, (codice,))
            riga = self.cursor.fetchone()
            
            if riga:
                # Ricostruzione dell'oggetto Prodotto (come in leggi_prodotti)
                codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo = riga
                
                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome,
                    prezzo_netto=float(prezzo_netto), 
                    aliquota_iva=float(aliquota_iva),
                )
                
                # Sovrascrive il Lordo con il valore del DB per coerenza (se necessario)
                # Prodotto ha già una logica corretta, quindi non è strettamente necessario, ma è una sicurezza
                # prodotto_ricostruito.prezzo_lordo = float(prezzo_lordo) 
                
                return prodotto_ricostruito
            else:
                return None # Prodotto non trovato
                
        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la ricerca: {e}")
            return None

        

    def aggiorna_prodotto(self, prodotto):
        """
        Aggiorna i dati di un prodotto esistente nel database, identificandolo tramite il codice.
        
        Args:
            prodotto (Prodotto): L'istanza di Prodotto con i dati aggiornati.
            
        Returns:
            bool: True se l'aggiornamento è riuscito, False altrimenti.
        """
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile aggiornare i dati.")
            return False

        # 1. Query SQL per l'aggiornamento
        # Vogliamo aggiornare tutti i campi che potrebbero essere cambiati, basandoci sul CODICE
        query = """
        UPDATE prodotti
        SET 
            nome = %s,
            prezzo_netto = %s,
            aliquota_iva = %s,
            prezzo_lordo = %s
        WHERE codice = %s;
        """
        
        # 2. Tupla dei Valori: l'ordine è cruciale!
        # NOTA: il codice va messo alla fine perché è il parametro della clausola WHERE
        valori = (
            prodotto.nome,
            prodotto.prezzo_netto,
            prodotto.aliquota_iva,
            prodotto.prezzo_lordo,
            prodotto.codice  # <--- Questo è il filtro WHERE
        )
        
        try:
            # Esecuzione della Query
            self.cursor.execute(query, valori)
            
            # Controlla quanti record sono stati modificati (dovrebbe essere 1)
            righe_aggiornate = self.cursor.rowcount
            
            if righe_aggiornate > 0:
                # 3. Conferma la Transazione
                self.conn.commit()
                print(f"✅ Aggiornamento completato per il prodotto '{prodotto.codice}'.")
                return True
            else:
                # Se rowcount è 0, il prodotto con quel codice non esiste
                print(f"⚠️ Errore: Prodotto con codice '{prodotto.codice}' non trovato. Nessun aggiornamento.")
                self.conn.rollback() # Annulla eventuali azioni intermedie
                return False
            
        except psycopg2.Error as e:
            # 4. Annulla la Transazione in caso di errore (es. dati non validi nel DB)
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore DB durante l'aggiornamento: {e}")
            return False
        
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return False


# ... (all'interno della classe ProdottoDBManager, dopo aggiorna_prodotto)

    def elimina_prodotto(self, codice):
        """
        Elimina un prodotto dal database, identificandolo tramite il codice.
        
        Args:
            codice (str): Il codice del prodotto da eliminare.
            
        Returns:
            bool: True se l'eliminazione è riuscita, False altrimenti.
        """
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile eliminare i dati.")
            return False

        # 1. Query SQL per l'eliminazione
        # NOTA: Usiamo il codice per identificare il record (il vincolo WHERE)
        query = "DELETE FROM prodotti WHERE codice = %s;"
        
        try:
            # Esecuzione della Query con il codice come parametro
            self.cursor.execute(query, (codice,))
            
            # Controlla quanti record sono stati eliminati (dovrebbe essere 1)
            righe_eliminate = self.cursor.rowcount
            
            if righe_eliminate > 0:
                # 2. Conferma la Transazione
                self.conn.commit()
                print(f"✅ Prodotto con codice '{codice}' eliminato con successo dal DB.")
                return True
            else:
                # Se rowcount è 0, il prodotto con quel codice non esisteva
                print(f"⚠️ Errore: Prodotto con codice '{codice}' non trovato. Nessuna eliminazione.")
                self.conn.rollback() 
                return False
            
        except psycopg2.Error as e:
            # 3. Annulla la Transazione in caso di errore
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore DB durante l'eliminazione: {e}")
            return False
        
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return False

# ... (all'interno della classe ProdottoDBManager) ...

    def ricerca_prodotti_filtrata(self, nome=None, prezzo_max=None):
        """
        Recupera prodotti filtrando per nome (LIKE) e/o prezzo netto massimo.
        
        Args:
            nome (str, optional): Filtra i prodotti il cui nome contiene questa stringa.
            prezzo_max (float, optional): Filtra i prodotti con prezzo netto inferiore o uguale a questo valore.
            
        Returns:
            list[Prodotto]: Una lista di istanze di oggetti Prodotto che soddisfano i criteri.
        """
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile eseguire la ricerca.")
            return []

        # 1. Base della Query
        query = "SELECT codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo FROM prodotti WHERE attivo = TRUE"
        condizioni = []
        valori = []

        # 2. Aggiunta Condizione per il Nome
        if nome:
            # Usiamo ILIKE per una ricerca case-insensitive e % per LIKE
            condizioni.append("nome ILIKE %s")
            valori.append(f"%{nome}%")

        # 3. Aggiunta Condizione per il Prezzo Massimo
        if prezzo_max is not None and prezzo_max >= 0:
            condizioni.append("prezzo_netto <= %s")
            valori.append(prezzo_max)

        # 4. Assemblaggio della Query
        if condizioni:
            query += " AND " + " AND ".join(condizioni)
        
        query += " ORDER BY nome ASC;"
        
        prodotti_letti = []
        
        try:
            # Esecuzione della Query con i valori dinamici
            self.cursor.execute(query, valori)
            risultati = self.cursor.fetchall()
            
            # Ricostruzione degli Oggetti (come in leggi_prodotti)
            for riga in risultati:
                codice, nome_db, prezzo_netto, aliquota_iva, prezzo_lordo, attivo = riga
                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome_db,
                    prezzo_netto=float(prezzo_netto),
                    aliquota_iva=float(aliquota_iva),
                )
                prodotti_letti.append(prodotto_ricostruito)

            print(f"✅ Ricerca completata. Trovati {len(prodotti_letti)} prodotti corrispondenti.")
            return prodotti_letti

        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la ricerca filtrata: {e}")
            return []
        except Exception as e:
            print(f"❌ Errore generico: {e}")
            return []