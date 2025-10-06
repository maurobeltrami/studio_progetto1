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

# -----------------------------------------------
# --- TEST DI CONNESSIONE E INSERIMENTO (CREATE) ---
# -----------------------------------------------
if __name__ == '__main__':
    
    # 1. Crea oggetti Prodotto validati in memoria
    try:
        laptop = Prodotto(codice="LPT-001", nome="Laptop Aziendale X1", prezzo_netto=850.00, aliquota_iva=22.0)
        tastiera = Prodotto(codice="ACS-012", nome="Tastiera Meccanica PRO", prezzo_netto=45.00, aliquota_iva=22.0)
        
    except ValueError as e:
        print(f"Errore di validazione Prodotto: {e}. Correggi la classe.py")
        exit()
        
    manager = ProdottoDBManager()
    print("\n--- Tentativo di connessione avviato ---")
    
    if manager.connetti():
        
        # TEST 1: Inserimento di un Prodotto Valido (Laptop)
        # Se LPT-001 è già presente, questo fallirà.
        print("\n--- TEST: Inserimento 1 ---")
        manager.inserisci_prodotto(laptop)
        
        # TEST 2: Inserimento di un altro Prodotto Valido (Tastiera)
        print("\n--- TEST: Inserimento 2 ---")
        manager.inserisci_prodotto(tastiera)
        
        print("\n--- TEST: Inserimento Duplicato ---")
        # TEST 3: Inserimento di un Prodotto DUPLICATO (dovrebbe fallire e attivare il ROLLBACK)
        laptop_duplicato = Prodotto(codice="LPT-001", nome="Laptop Duplicato", prezzo_netto=1.00, aliquota_iva=22.0)
        manager.inserisci_prodotto(laptop_duplicato) 
        
    manager.disconnetti()