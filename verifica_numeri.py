import requests
import csv

# Inserisci il tuo API key di Numverify
api_key = "b25f3ee50ed063253a243b9197f601bb"

# File CSV di input con i numeri da verificare (deve essere nella stessa cartella dello script)
csv_input = "numeri_input.csv"

# File CSV di output dove verranno salvati i risultati (nella stessa cartella dello script)
csv_output = "risultati_verifica.csv"

# Funzione per leggere i numeri dal file CSV
def leggi_numeri_da_csv(nome_file):
    numeri = []
    with open(nome_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            numeri.append(row["Numero"].strip())  # Rimuove eventuali spazi
    return numeri

# Funzione per verificare i numeri con Numverify
def verifica_numeri(numeri):
    risultati = []
    for numero in numeri:
        url = f"http://apilayer.net/api/validate?access_key={api_key}&number={numero}&country_code=&format=1"
        response = requests.get(url)
        dati = response.json()

        if "valid" in dati:
            risultato = {
                "Numero": numero,
                "Valido": dati["valid"],
                "Operatore": dati.get("carrier", "N/A"),
                "Paese": dati.get("country_name", "N/A"),
                "Tipo Linea": dati.get("line_type", "N/A")  # Aggiunto tipo di linea
            }
            risultati.append(risultato)
            print(f"Verificato: {risultato}")
        else:
            print(f"Errore con il numero {numero}")

    return risultati

# Funzione per salvare i dati in un file CSV
def salva_csv(dati, nome_file):
    with open(nome_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["Numero", "Valido", "Operatore", "Paese", "Tipo Linea"])
        writer.writeheader()
        writer.writerows(dati)
    print(f"Dati salvati in {nome_file}")

# Esegui il flusso completo
numeri = leggi_numeri_da_csv(csv_input)
risultati = verifica_numeri(numeri)
salva_csv(risultati, csv_output)
