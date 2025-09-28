def calcola_iva(prezzo_base):

	aliquota_iva = 0.22
	iva_calcolata = prezzo_base * aliquota_iva
	prezzo_finale = prezzo_base + iva_calcolata
	return prezzo_base, iva_calcolata, prezzo_finale, aliquota_iva

dati_csv = []

intestazione = ["Nome Prodotto", "Prezzo Base", "IVA Calcolata", "Prezzo Finale", "Aliquota"]
dati_csv.append(intestazione)

# Esempio 1: Laptop
pb_laptop, iva_laptop, pf_laptop, ali_laptop = calcola_iva(1500.00)
dati_csv.append(["Laptop", pb_laptop, iva_laptop, pf_laptop, ali_laptop])

# Esempio 2: Smartphone
pb_smartphone, iva_smartphone, pf_smartphone, ali_smartphone = calcola_iva(450.00)
dati_csv.append(["Smartphone", pb_smartphone, iva_smartphone, pf_smartphone, ali_smartphone])

# Esempio 3: Caricabatterie
pb_caricabatterie, iva_caricabatterie, pf_caricabatterie, ali_caricabatterie = calcola_iva(20.00)
dati_csv.append(["Caricabatterie", pb_caricabatterie, iva_caricabatterie, pf_caricabatterie, ali_caricabatterie])

# esempio 4 : Cuffie
pb_cuffie, iva_cuffie, pf_cuffie, ali_cuffie = calcola_iva(10.00)
dati_csv.append(["Cuffie", pb_cuffie, iva_cuffie, pf_cuffie, ali_cuffie])

import csv # Importa il modulo standard

nome_file = 'report_iva.csv'

# 'with open(...)' apre e chiude il file automaticamente, anche in caso di errore
# 'w' sta per modalità "write" (scrittura)
# 'newline=' assicura che non vengano aggiunte righe vuote tra i dati
with open(nome_file, 'w', newline='', encoding='utf-8') as file_csv:
    # csv.writer crea l'oggetto che scrive nel formato CSV
    scrittore = csv.writer(file_csv, delimiter=';') 
    
    # Scrive tutte le righe di dati_csv nel file
    scrittore.writerows(dati_csv)

print(f"\nReport IVA salvato con successo nel file: {nome_file}")
