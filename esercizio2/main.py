import sys
# Importiamo il manager del database
from .db_manager import ProdottoDBManager

# Il manager sarà l'oggetto principale che gestisce la connessione al DB
db_manager = ProdottoDBManager()

# --- Funzioni di Stampa ---

def mostra_menu():
    """Stampa le opzioni disponibili per l'utente."""
    print("\n" + "="*40)
    print("        MENU PRINCIPALE (GESTIONE PRODOTTI)")
    print("="*40)
    print("1. Visualizza tutti i prodotti")
    print("2. Inserisci nuovo prodotto (CREATE)")
    print("3. Aggiorna un prodotto (UPDATE)")
    print("4. Elimina un prodotto (DELETE)")
    print("5. Esegui Ricerca Avanzata (Filtri)")
    print("0. Esci e Chiudi Connessione")
    print("="*40)

def mostra_prodotti(lista_prodotti):
    """Visualizza la lista dei prodotti in un formato leggibile."""
    if not lista_prodotti:
        print("\n⚠️ Nessun prodotto trovato nel database.")
        return

    print("\n--- ELENCO PRODOTTI ATTIVI ---")
    print(f"{'Codice':<12} {'Nome':<30} {'Netto':>10} {'Lord/o':>10} {'IVA%':>5}")
    print("-" * 65)
    
    for p in lista_prodotti:
        print(f"{p.codice:<12} {p.nome:<30} {p.prezzo_netto:10.2f} {p.prezzo_lordo:10.2f} {p.aliquota_iva:5.0f}")
    print("-" * 65)
# --- Funzioni di Gestione Prodotto ---
from .classe import Prodotto 

def inserisci_nuovo_prodotto():
    """Gestisce l'input interattivo per creare e inserire un nuovo prodotto."""
    print("\n--- INSERIMENTO NUOVO PRODOTTO (CREATE) ---")
    
    # Acquisizione dati dall'utente
    codice = input("Codice Prodotto: ").strip()
    nome = input("Nome Prodotto: ").strip()
    
    try:
        prezzo_netto = float(input("Prezzo Netto: "))
        aliquota_iva = float(input("Aliquota IVA (%): "))
        
        # 1. Crea l'oggetto Prodotto in memoria (attiva la validazione e il calcolo Lordo)
        nuovo_prodotto = Prodotto(
            codice=codice, 
            nome=nome, 
            prezzo_netto=prezzo_netto, 
            aliquota_iva=aliquota_iva
        )
        
        # Mostra i dati calcolati prima di salvare
        print(f"\nProdotto pronto per il salvataggio:")
        print(f"  Netto: €{nuovo_prodotto.prezzo_netto:.2f}, Lordo: €{nuovo_prodotto.prezzo_lordo:.2f}")

        # 2. Chiama il metodo del DB Manager per l'inserimento
        db_manager.inserisci_prodotto(nuovo_prodotto)
        
    except ValueError as e:
        # Cattura gli errori di conversione (se l'utente non inserisce un numero)
        print(f"\n❌ Errore di Input: Devi inserire un numero valido per prezzo o IVA. Dettaglio: {e}")
        
    except Exception as e:
        # Cattura gli errori di validazione della classe Prodotto o errori DB (es. codice duplicato)
        print(f"\n❌ Operazione fallita. Dettaglio: {e}")


def aggiorna_prodotto_interattivo():
    """Gestisce l'input interattivo per aggiornare un prodotto esistente."""
    print("\n--- AGGIORNAMENTO PRODOTTO (UPDATE) ---")
    
    codice = input("Inserisci il Codice del prodotto da aggiornare: ").strip()
    
    # 1. Recupera il prodotto dal DB
    prodotto = db_manager.leggi_prodotto_per_codice(codice)
    
    if not prodotto:
        print(f"❌ Errore: Prodotto con codice '{codice}' non trovato.")
        return

    # Visualizza i dati attuali
    print("\n--- Dati Attuali ---")
    print(f"Nome: {prodotto.nome}")
    print(f"Prezzo Netto: €{prodotto.prezzo_netto:.2f}")
    print(f"Aliquota IVA: {prodotto.aliquota_iva:.0f}%")
    print("-" * 20)
    
    # 2. Acquisisci i nuovi valori
    try:
        # Acquisizione del NUOVO nome (o lascia vuoto per non modificare)
        nuovo_nome = input(f"Nuovo Nome (Attuale: {prodotto.nome}) - [Invio per lasciare invariato]: ").strip()
        
        # Acquisizione del NUOVO prezzo netto
        nuovo_netto_str = input(f"Nuovo Prezzo Netto (Attuale: €{prodotto.prezzo_netto:.2f}) - [Invio per lasciare invariato]: ").strip()
        
        # 3. Applica le modifiche all'oggetto in memoria
        
        # Aggiorna il nome solo se l'utente ha inserito un valore
        if nuovo_nome:
            prodotto.nome = nuovo_nome
            
        # Aggiorna il prezzo netto solo se l'utente ha inserito un valore
        if nuovo_netto_str:
            nuovo_netto = float(nuovo_netto_str)
            # La chiamata a aggiorna_prezzo_netto usa il setter, che include la validazione e ricalcola il Lordo
            prodotto.aggiorna_prezzo_netto(nuovo_netto)

        # 4. Salva le modifiche nel database
        db_manager.aggiorna_prodotto(prodotto)
        
        # Lettura di verifica
        prodotto_aggiornato = db_manager.leggi_prodotto_per_codice(codice)
        if prodotto_aggiornato:
            print(f"\n✅ Aggiornamento verificato: Netto finale: €{prodotto_aggiornato.prezzo_netto:.2f}, Lordo finale: €{prodotto_aggiornato.prezzo_lordo:.2f}")

    except ValueError:
        print("\n❌ Errore di Input: Devi inserire un numero valido per il prezzo.")
        
    except Exception as e:
        print(f"\n❌ Operazione fallita: {e}")


def elimina_prodotto_interattivo():
    """Gestisce l'input interattivo per eliminare un prodotto."""
    print("\n--- ELIMINAZIONE PRODOTTO (DELETE) ---")
    
    codice = input("Inserisci il Codice del prodotto da eliminare: ").strip()
    
    # 1. Recupera il prodotto per conferma visiva
    prodotto = db_manager.leggi_prodotto_per_codice(codice)
    
    if not prodotto:
        print(f"❌ Errore: Prodotto con codice '{codice}' non trovato.")
        return

    # 2. Richiesta di conferma
    print("\n--- ATTENZIONE: Conferma Eliminazione ---")
    print(f"Stai per eliminare: {prodotto.nome} (Codice: {prodotto.codice})")
    
    conferma = input("Sei sicuro di voler procedere? (S/N): ").strip().upper()
    
    if conferma == 'S':
        try:
            # 3. Chiama il metodo del DB Manager per l'eliminazione
            db_manager.elimina_prodotto(codice)
            print(f"\n✅ Prodotto '{codice}' eliminato con successo.")
            
        except Exception as e:
            print(f"\n❌ Operazione fallita. Dettaglio: {e}")
    else:
        print("\nOperazione annullata dall'utente.")

def ricerca_avanzata_interattiva():
    """Gestisce l'input interattivo per la ricerca filtrata."""
    print("\n--- RICERCA AVANZATA (FILTRI) ---")
    
    # Parametro 1: Nome (opzionale)
    nome_filtro = input("Filtra per Nome (parola chiave, Invio per ignorare): ").strip()
    
    # Parametro 2: Prezzo Massimo (opzionale)
    prezzo_max_input = input("Prezzo Netto Massimo (€, Invio per ignorare): ").strip()
    
    prezzo_max_filtro = None
    
    try:
        if prezzo_max_input:
            prezzo_max_filtro = float(prezzo_max_input)
            if prezzo_max_filtro < 0:
                 raise ValueError("Il prezzo massimo non può essere negativo.")
        
        # Chiama il metodo del DB Manager con i parametri raccolti
        risultati = db_manager.ricerca_prodotti_filtrata(
            nome=nome_filtro if nome_filtro else None,
            prezzo_max=prezzo_max_filtro
        )
        
        # Mostra i risultati usando la funzione esistente
        mostra_prodotti(risultati)

    except ValueError as e:
        print(f"\n❌ Errore di Input: {e}")
    except Exception as e:
        print(f"\n❌ Errore durante l'esecuzione della ricerca: {e}")
def avvia_cli():
    """Funzione principale che esegue il loop del menu."""
    if not db_manager.connetti():
        print("Impossibile avviare l'applicazione senza connessione al database.")
        sys.exit(1)

    while True:
        mostra_menu()
        scelta = input("Seleziona un'opzione (0-5): ").strip()

        if scelta == '1':
            # READ (Visualizza)
            prodotti = db_manager.leggi_prodotti()
            mostra_prodotti(prodotti)
            
        # ... all'interno di def avvia_cli():

        elif scelta == '2':
            # PRIMA: print("Funzione Inserimento (CREATE) non ancora implementata.")
            # DOPO: Chiama la funzione implementata
            inserisci_nuovo_prodotto() 
            
            
        elif scelta == '3':
            # CHIAMA LA FUNZIONE DI AGGIORNAMENTO
            aggiorna_prodotto_interattivo()
            
        elif scelta == '4':
            # CHIAMA LA FUNZIONE DI ELIMINAZIONE
            elimina_prodotto_interattivo()
            
        elif scelta == '5':
            # CHIAMA LA FUNZIONE DI RICERCA AVANZATA
            ricerca_avanzata_interattiva()
            
        elif scelta == '0':
            print("\nChiusura dell'applicazione...")
            db_manager.disconnetti()
            break
            
        else:
            print("\n❌ Opzione non valida. Riprova.")

if __name__ == '__main__':
    avvia_cli()