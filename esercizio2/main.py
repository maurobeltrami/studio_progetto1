import sys
import os
from .classe import Prodotto, Fornitore
from .db_manager import ProdottoDBManager

# Inizializzazione del Database Manager
db_manager = ProdottoDBManager()

def mostra_menu():
    print("\n==================================")
    print("      GESTIONALE PRODOTTI (ERP)")
    print("==================================")
    print("1. Inserisci Nuovo Prodotto")
    print("2. Visualizza Tutti i Prodotti")
    print("3. Cerca Prodotto per Codice")
    print("4. Aggiorna Prezzo Prodotto")
    print("5. Ricerca Avanzata (Filtri)")
    print("6. Elimina Prodotto (Soft Delete)")
    print("7. Mostra Fornitori ")
    print("0. Esci e Chiudi Connessione")
    print("==================================")

def mostra_prodotti(prodotti):
    if not prodotti:
        print("--- Nessun prodotto trovato. ---")
        return
    
    print("\n==============================")
    print("  ELENCO PRODOTTI ATTIVI")
    print("==============================")
    for p in prodotti:
        forn_info = f" ({p.fornitore.nome})" if p.fornitore else ""
        print(f"[{p.codice}] {p.nome}{forn_info} | Netto: €{p.prezzo_netto:.2f} | Lordo: €{p.prezzo_lordo:.2f}")
    print("==============================")


def leggi_fornitori_interattiva():
    """Permette all'utente di selezionare un fornitore esistente."""
    fornitori = db_manager.leggi_tutti_i_fornitori()
    
    if not fornitori:
        print("⚠️ Attenzione: Nessun fornitore trovato nel DB. Il prodotto sarà senza fornitore.")
        return None

    print("\n--- SELEZIONE FORNITORE ---")
    print("0. Nessun Fornitore")
    
    for i, f in enumerate(fornitori):
        print(f"{f.id_fornitore}. {f.nome}")
        
    while True:
        scelta = input("Seleziona ID Fornitore (0 per ignorare): ").strip()
        if not scelta:
            print("⚠️ Selezione omessa. Prodotto senza fornitore.")
            return None
            
        try:
            id_scelto = int(scelta)
            if id_scelto == 0:
                return None
            
            forn_selezionato = next((f for f in fornitori if f.id_fornitore == id_scelto), None)
            
            if forn_selezionato:
                print(f"✅ Fornitore selezionato: {forn_selezionato.nome}")
                return forn_selezionato
            else:
                print("❌ ID non valido. Riprova.")
        except ValueError:
            print("❌ Input non valido. Inserisci un numero intero.")


def inserisci_prodotto_interattivo():
    print("\n--- INSERIMENTO NUOVO PRODOTTO ---")
    
    codice = input("Codice Prodotto: ").strip()
    nome = input("Nome Prodotto: ").strip()
    
    # Selezione Fornitore (Many2one)
    fornitore_selezionato = leggi_fornitori_interattiva()
    
    try:
        prezzo_netto = float(input("Prezzo Netto (€): "))
        aliquota_iva_input = input("Aliquota IVA (% - Invio per 22.0): ")
        aliquota_iva = float(aliquota_iva_input) if aliquota_iva_input else 22.0
        
        nuovo_prodotto = Prodotto(
            codice=codice,
            nome=nome,
            prezzo_netto=prezzo_netto,
            aliquota_iva=aliquota_iva,
            fornitore=fornitore_selezionato
        )
        
        db_manager.inserisci_prodotto(nuovo_prodotto)
        
    except ValueError as e:
        print(f"\n❌ Errore di Input o Validazione: {e}")
    except Exception as e:
        print(f"\n❌ Errore generico: {e}")

def visualizza_tutti_interattivo():
    prodotti = db_manager.leggi_prodotti()
    mostra_prodotti(prodotti)

def cerca_per_codice_interattivo():
    print("\n--- RICERCA PER CODICE ---")
    codice = input("Inserisci il Codice Prodotto da cercare: ").strip()
    
    prodotto = db_manager.leggi_prodotto_per_codice(codice)
    
    if prodotto:
        print("\n✅ Prodotto Trovato:")
        print(prodotto)
    else:
        print(f"❌ Prodotto con codice '{codice}' non trovato o non attivo.")

def aggiorna_prodotto_interattivo():
    print("\n--- AGGIORNAMENTO PREZZO ---")
    codice = input("Codice Prodotto da aggiornare: ").strip()
    
    prodotto = db_manager.leggi_prodotto_per_codice(codice)
    
    if prodotto:
        print(f"Attuale prezzo Netto per '{prodotto.nome}': €{prodotto.prezzo_netto:.2f}")
        try:
            nuovo_netto = float(input("Nuovo Prezzo Netto (€): "))
            
            prodotto.aggiorna_prezzo_netto(nuovo_netto)
            db_manager.aggiorna_prodotto(prodotto)
            
        except ValueError:
            print("❌ Input non valido. Il prezzo deve essere un numero.")
        except Exception as e:
            print(f"❌ Errore durante l'aggiornamento: {e}")
    else:
        print(f"❌ Prodotto con codice '{codice}' non trovato.")

def elimina_prodotto_interattivo():
    print("\n--- ELIMINAZIONE PRODOTTO ---")
    codice = input("Codice Prodotto da ELIMINARE: ").strip()
    
    if db_manager.elimina_prodotto(codice):
        print(f"✅ Prodotto {codice} eliminato con successo.")
    else:
        print(f"❌ Impossibile eliminare il prodotto {codice}.")

def ricerca_avanzata_interattiva():
    print("\n--- RICERCA AVANZATA (FILTRI) ---")
    
    nome_filtro = input("Filtra per Nome (parola chiave, Invio per ignorare): ").strip()
    prezzo_max_input = input("Prezzo Netto Massimo (€, Invio per ignorare): ").strip()
    
    prezzo_max_filtro = None
    
    try:
        if prezzo_max_input:
            prezzo_max_filtro = float(prezzo_max_input)
            if prezzo_max_filtro < 0:
                 raise ValueError("Il prezzo massimo non può essere negativo.")
        
        risultati = db_manager.ricerca_prodotti_filtrata(
            nome=nome_filtro if nome_filtro else None,
            prezzo_max=prezzo_max_filtro
        )
        
        mostra_prodotti(risultati)

    except ValueError as e:
        print(f"\n❌ Errore di Input: {e}")
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione della ricerca: {e}")

def visualizza_fornitori_interattivo():
    """Recupera e mostra tutti i fornitori presenti nel database."""
    print("\n--- ELENCO FORNITORI ATTIVI ---")
    
    fornitori = db_manager.leggi_tutti_i_fornitori()
    
    if not fornitori:
        print("--- Nessun fornitore trovato. ---")
        return
        
    for f in fornitori:
        print(f"[ID: {f.id_fornitore}] Nome: {f.nome}")
    print("-------------------------------")

def avvia_cli():
    print("--- Avvio CLI del Gestionale Prodotto ---")
    if not db_manager.connetti():
        print("Impossibile connettersi al database. Uscita.")
        sys.exit(1)

    while True:
        mostra_menu()
        scelta = input("Seleziona un'opzione (0-7): ").strip()

        if scelta == '1':
            inserisci_prodotto_interattivo()
        elif scelta == '2':
            visualizza_tutti_interattivo()
        elif scelta == '3':
            cerca_per_codice_interattivo()
        elif scelta == '4':
            aggiorna_prodotto_interattivo()
        elif scelta == '5':
            ricerca_avanzata_interattiva()
        elif scelta == '6':
            elimina_prodotto_interattivo()
        elif scelta == '7':
            visualizza_fornitori_interattivo()
        elif scelta == '0':
            print("Uscita in corso...")
            break
        else:
            print("❌ Opzione non valida. Riprova.")

    db_manager.disconnetti()
    print("Programma terminato.")

if __name__ == '__main__':
    # Assicurati che l'ambiente sia impostato per l'esecuzione del modulo
    # Aggiungi la directory superiore al PYTHONPATH per l'importazione
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    avvia_cli()