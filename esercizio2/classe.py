class Prodotto:
	def __init__(self, codice,nome, prezzo_netto, aliquota_iva=0.22):
		
		#1.chiamata alla validazione
		self._valida_dati(codice, nome, prezzo_netto, aliquota_iva)
	
		#se la validazione non ha sollevato eccezioni, salva i dati
		self.codice = codice
		self.nome = nome
		self.prezzo_netto = prezzo_netto
		self.aliquota_iva = aliquota_iva
		
		self.prezzo_lordo = self.calcola_prezzo_lordo()

	#metodo di validazione separato
	def _valida_dati(self, codice, nome, prezzo_netto, aliquota_iva):
		"""Solleva eccezioni integrate se i dati violano le regole ERP."""
		if not codice or not nome:
			#solleva un errore generico se un campo è essenziale è vuoto
			raise ValueError("Il codice e il nome del prodotto non possono essere vuoti.")
		if prezzo_netto < 0:
			#solleva un errore specifico per dati numerici non validi
			raise ValueError(f"Il prezzo netto(€{prezzo_netto:.2f}) non può essere negativo.")
		if aliquota_iva < 0:
			#stessa regola per l'IVA
			raise ValueError(f"L'aliquota IVA (€{aliquota_iva*100:.0f}) non può essere negativa.")

	def calcola_prezzo_lordo(self):
		"""Calcola il prezzo lordo (netto + IVA) del prodotto."""
		return self.prezzo_netto * (1 + self.aliquota_iva)
	
	def __str__(self):
		iva_perc = self.aliquota_iva * 100
		return (f"\n--- dettagli prodotto ---\n"
			f"Codice: {self.codice}\n"
			f"Nome: {self.nome}\n"
			f"Prezzo Netto: €{self.prezzo_netto:.2f}\n"
			f"Aliquota IVA: {iva_perc: .0f}%\n"
			f"Prezzo Lordo: €{self.prezzo_lordo:.2f}")
	
	def aggiorna_prezzo(self, nuovo_prezzo_netto):
		"""Aggiorna il prezzo netto e ricalcola immediatamente il prezzo lordo."""
		#1. Aggiorna l'attributo principale
		self.prezzo_netto = nuovo_prezzo_netto
		#2. Ricalcola l'attributo dipendente
		self.prezzo_lordo = self.calcola_prezzo_lordo()
		print(f"\nPrezzo di '{self.nome}' aggiornato a €{self.prezzo_netto:.2f} (Netto).")

#1. CREATE: Creazione delle istanze

try:
	laptop = Prodotto(codice="LPT-001",nome="Laptop Aziendale X1" ,prezzo_netto=850.00)
	print(f"Successo: Creato {laptop.nome}")
except ValueError as e:
	#questa parte non dovrebbe essere eseguita
	print(f"Errore inaspettato durante creazione valida: {e}")

#Test negativo1 (prezzo negativo)
try:
	prodotto_negativo = Prodotto(codice="ERR-001", nome="Prodotto Negativo", prezzo_netto=-10.00)
	# Se il codice arriva qui, la validazione è fallita
	print("Errore! La validazione del prezzo negativo ha fallito.")
except ValueError as e:
	#cattura l'eccezione sollevata da _valida_dati
	print(f"Eccezione catturata (Prezzo negativo): {e}")

#Test negativo2 (Nome vuoto)
try:
        prodotto_vuoto = Prodotto(codice="ERR-002", nome="", prezzo_netto=50.00)
        # Se il codice arriva qui, la validazione è fallita
        print("Errore! La validazione del nome vuoto ha fallito.")
except ValueError as e:
        #cattura l'eccezione sollevata da _valida_dati
        print(f"Eccezione catturata (Nome vuoto): {e}")

tastiera = Prodotto(
	codice="ACS-012",
	nome="Tastiera",
	prezzo_netto=45.00
)

licenza_software = Prodotto(
	codice="SW-LIC-PRO",
	nome="licenza ERP Pro",
	prezzo_netto=1200.00,
	aliquota_iva=0.00
)

#2. READ: Stampa dei risultati
print(laptop)
print(tastiera)
print(licenza_software)

# UPDATE: modifica del prezzo
laptop.aggiorna_prezzo(nuovo_prezzo_netto=799.99)
print(laptop)

#4. DELETE: Eliminazione dell'oggetto 'tastiera'
print("\n---Operazione DELETE ---")
print("Eliminazione dell'oggetto 'tastiera' con del...")
del tastiera
print("Oggetto 'tastiera' non più accessibile.")




