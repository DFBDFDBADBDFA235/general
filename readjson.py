import json

def read_from_json(filename="data.json"):
    """
    Legge i dati da un file JSON e li restituisce come una struttura dati Python.

    Args:
        filename (str, optional): Il nome del file JSON da leggere.
                                   Defaults to "data.json".

    Returns:
        list or dict or None: La struttura dati letta dal file JSON.
                             Restituisce None in caso di errore o se il file è vuoto.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
        print(f"Dati letti con successo da '{filename}'.")
        return data
    except FileNotFoundError:
        print(f"Errore: Il file '{filename}' non è stato trovato.")
        return None
    except json.JSONDecodeError:
        print(f"Errore: Il file '{filename}' non contiene un JSON valido.")
        return None
    except Exception as e:
        print(f"Si è verificato un errore durante la lettura dal JSON: {e}")
        return None

if __name__ == '__main__':
    # Esempio di lettura dei dati salvati
    loaded_data = read_from_json()
    if loaded_data:
        print("Dati caricati:")
        print(loaded_data)
