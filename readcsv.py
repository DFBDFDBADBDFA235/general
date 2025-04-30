import csv

def read_from_csv(filename="data.csv"):
    """
    Legge i dati da un file CSV e li restituisce come una lista di dizionari.

    Args:
        filename (str, optional): Il nome del file CSV da leggere.
                                   Defaults to "data.csv".

    Returns:
        list of dict: Una lista di dizionari, dove ogni dizionario
                      rappresenta una riga del CSV. Restituisce una lista vuota
                      in caso di errore o se il file è vuoto.
    """
    data = []
    try:
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        print(f"Dati letti con successo da '{filename}'.")
    except FileNotFoundError:
        print(f"Errore: Il file '{filename}' non è stato trovato.")
    except Exception as e:
        print(f"Si è verificato un errore durante la lettura dal CSV: {e}")
    return data

if __name__ == '__main__':
    # Esempio di lettura dei dati salvati
    loaded_data = read_from_csv()
    if loaded_data:
        print("Dati caricati:")
        for row in loaded_data:
            print(row)
