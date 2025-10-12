import psycopg2
import os
from dotenv import load_dotenv
from classe import Prodotto, Fornitore

load_dotenv() 

DB_CONFIG = {
    "host": "localhost",
    "database": os.environ.get("DB_NAME", "studio_progetto_erp"),
    "user": os.environ.get("DB_USER", "mauroi"),
    "password": os.environ.get("DB_PASSWORD", "la_tua_password_segreta")
}

class ProdottoDBManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connetti(self):
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
            print("✅ Connessione a PostgreSQL riuscita.")
            return True
        except psycopg2.Error as e:
            print(f"❌ Errore durante la connessione a PostgreSQL: {e}")
            return False

    def disconnetti(self):
        if self.cursor:
            self.cursor.close()
            
        if self.conn and not self.conn.closed:
            self.conn.close()
            print("✅ Connessione a PostgreSQL chiusa.")

    def inserisci_prodotto(self, prodotto):
        id_fornitore_da_salvare = prodotto.fornitore.id_fornitore if prodotto.fornitore else None
        
        query = """
        INSERT INTO prodotti (codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, id_fornitore)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id; 
        """
        
        valori = (
            prodotto.codice,
            prodotto.nome,
            prodotto.prezzo_netto,
            prodotto.aliquota_iva,
            prodotto.prezzo_lordo,
            id_fornitore_da_salvare
        )
        
        try:
            self.cursor.execute(query, valori)
            nuovo_id = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f"✅ Prodotto '{prodotto.nome}' inserito con successo! ID DB: {nuovo_id}")
            return nuovo_id
            
        except psycopg2.Error as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore DB durante l'inserimento: {e}")
            return None
        
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return None

    def leggi_prodotti(self):
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile leggere i dati.")
            return []
            
        query = """
        SELECT 
            p.codice, p.nome, p.prezzo_netto, p.aliquota_iva, p.prezzo_lordo, p.attivo,
            f.id, f.nome
        FROM prodotti p
        LEFT JOIN fornitori f ON p.id_fornitore = f.id
        WHERE p.attivo = TRUE
        ORDER BY p.nome ASC;
        """
        
        prodotti_letti = []
        
        try:
            self.cursor.execute(query)
            risultati = self.cursor.fetchall()
            
            for riga in risultati:
                codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo, id_fornitore_db, nome_fornitore_db = riga
                
                fornitore_obj = None
                if id_fornitore_db is not None and nome_fornitore_db is not None:
                    fornitore_obj = Fornitore(id_fornitore=id_fornitore_db, nome=nome_fornitore_db)

                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome,
                    prezzo_netto=float(prezzo_netto),
                    aliquota_iva=float(aliquota_iva),
                    fornitore=fornitore_obj
                )
                
                prodotti_letti.append(prodotto_ricostruito)

            print(f"✅ Lettura completata. Trovati {len(prodotti_letti)} prodotti attivi.")
            return prodotti_letti

        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la lettura dei prodotti: {e}")
            return []
        except Exception as e:
            print(f"❌ Errore generico durante la ricostruzione dei prodotti: {e}")
            return []

    def leggi_prodotto_per_codice(self, codice):
        if not self.conn:
            return None
            
        query = """
        SELECT 
            p.codice, p.nome, p.prezzo_netto, p.aliquota_iva, p.prezzo_lordo, p.attivo,
            f.id, f.nome
        FROM prodotti p
        LEFT JOIN fornitori f ON p.id_fornitore = f.id
        WHERE p.codice = %s AND p.attivo = TRUE;
        """
        
        try:
            self.cursor.execute(query, (codice,))
            riga = self.cursor.fetchone()
            
            if riga:
                codice, nome, prezzo_netto, aliquota_iva, prezzo_lordo, attivo, id_fornitore_db, nome_fornitore_db = riga
                
                fornitore_obj = None
                if id_fornitore_db is not None and nome_fornitore_db is not None:
                    fornitore_obj = Fornitore(id_fornitore=id_fornitore_db, nome=nome_fornitore_db)
                
                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome,
                    prezzo_netto=float(prezzo_netto), 
                    aliquota_iva=float(aliquota_iva),
                    fornitore=fornitore_obj
                )
                
                return prodotto_ricostruito
            else:
                return None 
                
        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la ricerca: {e}")
            return None
        except Exception as e:
            print(f"❌ Errore generico durante la ricostruzione del prodotto: {e}")
            return None
        

    def aggiorna_prodotto(self, prodotto):
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile aggiornare i dati.")
            return False

        query = """
        UPDATE prodotti
        SET 
            nome = %s,
            prezzo_netto = %s,
            aliquota_iva = %s,
            prezzo_lordo = %s
        WHERE codice = %s;
        """
        
        valori = (
            prodotto.nome,
            prodotto.prezzo_netto,
            prodotto.aliquota_iva,
            prodotto.prezzo_lordo,
            prodotto.codice
        )
        
        try:
            self.cursor.execute(query, valori)
            righe_aggiornate = self.cursor.rowcount
            
            if righe_aggiornate > 0:
                self.conn.commit()
                print(f"✅ Aggiornamento completato per il prodotto '{prodotto.codice}'.")
                return True
            else:
                print(f"⚠️ Errore: Prodotto con codice '{prodotto.codice}' non trovato. Nessun aggiornamento.")
                self.conn.rollback() 
                return False
            
        except psycopg2.Error as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore DB durante l'aggiornamento: {e}")
            return False
        
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return False

    def elimina_prodotto(self, codice):
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile eliminare i dati.")
            return False

        query = "DELETE FROM prodotti WHERE codice = %s;"
        
        try:
            self.cursor.execute(query, (codice,))
            righe_eliminate = self.cursor.rowcount
            
            if righe_eliminate > 0:
                self.conn.commit()
                print(f"✅ Prodotto con codice '{codice}' eliminato con successo dal DB.")
                return True
            else:
                print(f"⚠️ Errore: Prodotto con codice '{codice}' non trovato. Nessuna eliminazione.")
                self.conn.rollback() 
                return False
            
        except psycopg2.Error as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore DB durante l'eliminazione: {e}")
            return False
        
        except Exception as e:
            if self.conn:
                self.conn.rollback()
            print(f"❌ Errore generico: {e}")
            return False

    def ricerca_prodotti_filtrata(self, nome=None, prezzo_max=None):
        if not self.conn:
            print("❌ Connessione non attiva. Impossibile eseguire la ricerca.")
            return []

        # La query usa la JOIN per poter includere i dati del fornitore nei risultati
        query = """
        SELECT 
            p.codice, p.nome, p.prezzo_netto, p.aliquota_iva, p.prezzo_lordo, p.attivo,
            f.id, f.nome
        FROM prodotti p
        LEFT JOIN fornitori f ON p.id_fornitore = f.id
        WHERE p.attivo = TRUE
        """
        
        condizioni = []
        valori = []

        if nome:
            condizioni.append("p.nome ILIKE %s")
            valori.append(f"%{nome}%")

        if prezzo_max is not None and prezzo_max >= 0:
            condizioni.append("p.prezzo_netto <= %s")
            valori.append(prezzo_max)

        if condizioni:
            query += " AND " + " AND ".join(condizioni)
        
        query += " ORDER BY p.nome ASC;"
        
        prodotti_letti = []
        
        try:
            self.cursor.execute(query, valori)
            risultati = self.cursor.fetchall()
            
            for riga in risultati:
                codice, nome_db, prezzo_netto, aliquota_iva, prezzo_lordo, attivo, id_fornitore_db, nome_fornitore_db = riga

                fornitore_obj = None
                if id_fornitore_db is not None and nome_fornitore_db is not None:
                    fornitore_obj = Fornitore(id_fornitore=id_fornitore_db, nome=nome_fornitore_db)

                prodotto_ricostruito = Prodotto(
                    codice=codice,
                    nome=nome_db,
                    prezzo_netto=float(prezzo_netto),
                    aliquota_iva=float(aliquota_iva),
                    fornitore=fornitore_obj
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
            
    def leggi_tutti_i_fornitori(self):
        """Recupera tutti i fornitori dal database."""
        if not self.conn:
            return []
        
        query = "SELECT id, nome FROM fornitori ORDER BY nome ASC;"
        fornitori_letti = []

        try:
            self.cursor.execute(query)
            risultati = self.cursor.fetchall()
            
            for id_db, nome_db in risultati:
                fornitori_letti.append(Fornitore(id_fornitore=id_db, nome=nome_db))
                
            return fornitori_letti
            
        except psycopg2.Error as e:
            print(f"❌ Errore DB durante la lettura dei fornitori: {e}")
            return []
        except Exception as e:
            print(f"❌ Errore generico: {e}")
            return []