import json

def save_to_json(data, filename="data.json"):
    """
    Salva una struttura dati Python (solitamente una lista o un dizionario)
    in un file JSON.

    Args:
        data (list or dict): La struttura dati da salvare.
        filename (str, optional): Il nome del file JSON da creare.
                                   Defaults to "data.json".
    """
    try:
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=4)  # 'indent=4' per una formattazione leggibile
        print(f"Dati salvati con successo in '{filename}'.")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio nel JSON: {e}")

if __name__ == '__main__':
    # Esempio di dati da salvare
    data_to_save = [
        {'nome': 'Alice', 'età': 30, 'città': 'Milano'},
        {'nome': 'Bob', 'età': 25, 'città': 'Roma'},
        {'nome': 'Charlie', 'età': 35, 'città': 'Napoli'}
    ]
    save_to_json(data_to_save)
