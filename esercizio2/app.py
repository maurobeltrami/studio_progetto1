# esercizi/esercizio2/app.py

import json
from flask import Flask, jsonify, request
import sys
import os

# Aggiusta il path per l'importazione dei moduli locali (db_manager e classe)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_manager import ProdottoDBManager
from classe import Prodotto, Fornitore

# Inizializzazione dell'Applicazione Flask e del Database Manager
app = Flask(__name__)
db_manager = ProdottoDBManager()

# Collegamento al DB all'avvio dell'applicazione
# Utilizziamo il contesto dell'applicazione Flask per la gestione della connessione
with app.app_context():
    if not db_manager.connetti():
        print("Errore: Impossibile connettersi al database all'avvio dell'API.")
        sys.exit(1)


# ==============================================================================
# 1. READ ALL (GET /api/v1/prodotti)
# ==============================================================================
@app.route('/api/v1/prodotti', methods=['GET'])
def get_prodotti():
    prodotti = db_manager.leggi_prodotti()
    
    # Trasforma la lista di oggetti Prodotto in una lista di dizionari per JSON
    prodotti_json = []
    for p in prodotti:
        # Serializzazione completa del Prodotto, includendo il fornitore
        fornitore_data = None
        if p.fornitore:
            fornitore_data = {
                'id': p.fornitore.id_fornitore,
                'nome': p.fornitore.nome
            }
            
        prodotti_json.append({
            'codice': p.codice,
            'nome': p.nome,
            'prezzo_netto': p.prezzo_netto,
            'prezzo_lordo': p.prezzo_lordo,
            'aliquota_iva': p.aliquota_iva,
            'fornitore': fornitore_data # <-- La relazione è qui
        })
        
    return jsonify(prodotti_json)

# ==============================================================================
# Esecuzione dell'App
# ==============================================================================
if __name__ == '__main__':
    # Quando l'applicazione si chiude, chiudiamo la connessione al DB
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        if db_manager:
            db_manager.disconnetti()
    
    print("--- API RESTful Prodotto avviata su http://127.0.0.1:5000 ---")
    app.run(debug=True)