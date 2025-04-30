import csv

def save_to_csv(data, filename="data.csv"):
    """
    Salva una lista di dizionari in un file CSV.

    Args:
        data (list of dict): La lista di dizionari da salvare.
                             Ogni dizionario rappresenta una riga nel CSV,
                             con le chiavi come intestazioni delle colonne.
        filename (str, optional): Il nome del file CSV da creare.
                                   Defaults to "data.csv".
    """
    if not data:
        print("Nessun dato da salvare nel CSV.")
        return

    fieldnames = data[0].keys()  # Ottieni le intestazioni delle colonne dalle chiavi del primo dizionario
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Scrivi la riga delle intestazioni
            writer.writerows(data)  # Scrivi tutte le righe di dati
        print(f"Dati salvati con successo in '{filename}'.")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio nel CSV: {e}")

if __name__ == '__main__':
    # Esempio di dati da salvare
    data_to_save = [
        {'nome': 'Alice', 'età': 30, 'città': 'Milano'},
        {'nome': 'Bob', 'età': 25, 'città': 'Roma'},
        {'nome': 'Charlie', 'età': 35, 'città': 'Napoli'}
    ]
    save_to_csv(data_to_save)
