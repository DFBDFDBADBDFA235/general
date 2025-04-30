import sqlite3

DATABASE_NAME = 'mydatabase.db'
TABLE_NAME = 'users'

def read_from_sqlite():
    """Legge tutti i dati dalla tabella nel database SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {TABLE_NAME}')
    rows = cursor.fetchall()
    conn.close()
    print(f"Dati letti con successo dalla tabella '{TABLE_NAME}'.")
    # Converti le tuple in dizionari per una migliore leggibilità
    columns = ['id', 'nome', 'età', 'città']
    return [dict(zip(columns, row)) for row in rows]

if __name__ == '__main__':
    loaded_data = read_from_sqlite()
    if loaded_data:
        print("Dati caricati da SQLite:")
        for row in loaded_data:
            print(row)
