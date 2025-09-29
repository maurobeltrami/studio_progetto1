class Prodotto:
	def __init__(self, codice,nome, prezzo_netto, aliquota_iva=0.22):
		self.codice = codice
		self.nome = nome
		self.prezzo_netto = prezzo_netto
		self.aliquota_iva = aliquota_iva
		
		self.prezzo_lordo = self.calcola_prezzo_lordo()

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

laptop = Prodotto(
	codice="LPT-001",
	nome="Laptop Aziendale X1" ,
	prezzo_netto=850.00
)

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




