import uuid
from decimal import Decimal, ROUND_HALF_UP

class Prodotto:
    """
    Gestisce il modello di dati di un Prodotto, inclusa la validazione,
    il calcolo del prezzo Lordo e la gestione dell'identificativo.
    """
    def __init__(self, codice, nome, prezzo_netto, aliquota_iva=22.0):
        # Genera un ID univoco in memoria (utile finché non usiamo l'ID del DB)
        self._uuid = str(uuid.uuid4())
        
        # Inizializza gli attributi privati
        self._codice = None
        self._nome = None
        self._prezzo_netto = None
        self._aliquota_iva = None
        self._prezzo_lordo = None
        
        # Assegna i valori tramite i setter (che includono la validazione)
        self.codice = codice
        self.nome = nome
        self.aliquota_iva = aliquota_iva
        self.prezzo_netto = prezzo_netto # Questo setter calcolerà anche il Lordo
        
    # --- Metodo di Calcolo Interno (Il Fix del Lordo) ---
    def _calcola_prezzo_lordo(self):
        """Calcola e imposta il prezzo Lordo basandosi su Netto e IVA."""
        if self._prezzo_netto is None or self._aliquota_iva is None:
            return

        # 1. Converte l'aliquota da percentuale (es. 22.0) a fattore (es. 1.22)
        # 🚨 FIX CRUCIALE: Assicura che l'aliquota sia divisa per 100
        fattore_moltiplicativo = Decimal(1) + (self._aliquota_iva / Decimal(100))
        
        # 2. Calcola e arrotonda il Lordo a 2 decimali
        lordo = self._prezzo_netto * fattore_moltiplicativo
        self._prezzo_lordo = lordo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
    # --- PROPRIETÀ (GETTERS E SETTERS) ---
    
    @property
    def codice(self):
        return self._codice
    
    @codice.setter
    def codice(self, value):
        if not value or not value.strip():
            raise ValueError("Il codice e il nome del prodotto non possono essere vuoti.")
        self._codice = value.strip()

    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, value):
        if not value or not value.strip():
            raise ValueError("Il codice e il nome del prodotto non possono essere vuoti.")
        self._nome = value.strip()

    @property
    def aliquota_iva(self):
        # Restituisce il valore come float per coerenza con il DB/input, anche se internamente è Decimal
        return float(self._aliquota_iva) 
    
    @aliquota_iva.setter
    def aliquota_iva(self, value):
        # Permette l'input come float o int
        iva = Decimal(str(value)) 
        if iva < 0:
            raise ValueError("L'aliquota IVA non può essere negativa.")
        self._aliquota_iva = iva
        # Ricalcola il Lordo se il Netto è già impostato
        self._calcola_prezzo_lordo() 

    @property
    def prezzo_netto(self):
        # Restituisce il valore come float (o Decimal)
        return float(self._prezzo_netto) if self._prezzo_netto else 0.0
    
    @prezzo_netto.setter
    def prezzo_netto(self, value):
        netto = Decimal(str(value)) 
        if netto < 0:
            raise ValueError(f"Il prezzo netto (€{netto:.2f}) non può essere negativo.")
        self._prezzo_netto = netto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # 💥 AZIONE CRUCIALE: Ricalcola il Lordo ogni volta che il Netto cambia
        self._calcola_prezzo_lordo() 

    @property
    def prezzo_lordo(self):
        return float(self._prezzo_lordo) if self._prezzo_lordo else 0.0

    # --- Metodi Pubblici ---

    def aggiorna_prezzo_netto(self, nuovo_netto):
        """Aggiorna il prezzo netto e ricalcola il prezzo lordo."""
        # Usa il setter per sfruttare la validazione e il ricalcolo automatico del Lordo
        self.prezzo_netto = nuovo_netto
        print(f"Prezzo di '{self.nome}' aggiornato a €{self.prezzo_netto:.2f} (Netto).")

    # --- Rappresentazione ---

    def __str__(self):
        """Definisce la rappresentazione a stringa dell'oggetto."""
        return (
            "--- dettagli prodotto ---\n"
            f"Codice: {self.codice}\n"
            f"Nome: {self.nome}\n"
            f"Prezzo Netto: €{self.prezzo_netto:.2f}\n"
            f"Aliquota IVA:  {self.aliquota_iva}%\n"
            f"Prezzo Lordo: €{self.prezzo_lordo:.2f}"
        )