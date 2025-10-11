import uuid
from decimal import Decimal, ROUND_HALF_UP

class Fornitore:
    def __init__(self, id_fornitore, nome):
        self._id = id_fornitore 
        self.nome = nome

    @property
    def id_fornitore(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        if not value or not value.strip():
            raise ValueError("Il nome del Fornitore non può essere vuoto.")
        self._nome = value.strip()
        
    def __str__(self):
        return f"Fornitore(ID: {self.id_fornitore}, Nome: {self.nome})"

    def __repr__(self):
        return self.__str__()

class Prodotto:
    def __init__(self, codice: str, nome: str, prezzo_netto: float, aliquota_iva: float = 22.0, fornitore: 'Fornitore' = None):
        self._uuid = str(uuid.uuid4())
        self._codice = None
        self._nome = None
        self._prezzo_netto = None
        self._aliquota_iva = None
        self._prezzo_lordo = None
        self._fornitore = None
        
        self.codice = codice
        self.nome = nome
        self.aliquota_iva = aliquota_iva
        self.prezzo_netto = prezzo_netto
        self.fornitore = fornitore 

    def _calcola_prezzo_lordo(self):
        if self._prezzo_netto is None or self._aliquota_iva is None:
            return
        fattore_moltiplicativo = Decimal(1) + (self._aliquota_iva / Decimal(100))
        lordo = self._prezzo_netto * fattore_moltiplicativo
        self._prezzo_lordo = lordo.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
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
        return float(self._aliquota_iva) 
    
    @aliquota_iva.setter
    def aliquota_iva(self, value):
        iva = Decimal(str(value)) 
        if iva < 0:
            raise ValueError("L'aliquota IVA non può essere negativa.")
        self._aliquota_iva = iva
        self._calcola_prezzo_lordo() 

    @property
    def prezzo_netto(self):
        return float(self._prezzo_netto) if self._prezzo_netto else 0.0
    
    @prezzo_netto.setter
    def prezzo_netto(self, value):
        netto = Decimal(str(value)) 
        if netto < 0:
            raise ValueError(f"Il prezzo netto (€{netto:.2f}) non può essere negativo.")
        self._prezzo_netto = netto.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self._calcola_prezzo_lordo() 

    @property
    def prezzo_lordo(self):
        return float(self._prezzo_lordo) if self._prezzo_lordo else 0.0

    @property
    def fornitore(self) -> 'Fornitore':
        return self._fornitore

    @fornitore.setter
    def fornitore(self, value):
        if value is not None and not isinstance(value, Fornitore):
            raise TypeError("L'attributo fornitore deve essere un'istanza della classe Fornitore o None.")
        self._fornitore = value

    def aggiorna_prezzo_netto(self, nuovo_netto):
        self.prezzo_netto = nuovo_netto
        print(f"Prezzo di '{self.nome}' aggiornato a €{self.prezzo_netto:.2f} (Netto).")

    def __str__(self):
        forn_info = f" (Fornitore: {self.fornitore.nome})" if self.fornitore else ""
        
        return (
            f"Prodotto(Codice: {self.codice}, Nome: {self.nome}{forn_info})\n"
            f"  Netto: €{self.prezzo_netto:.2f}, Lordo: €{self.prezzo_lordo:.2f}, IVA: {self.aliquota_iva}%"
        )
        
    def __repr__(self):
        return self.__str__()