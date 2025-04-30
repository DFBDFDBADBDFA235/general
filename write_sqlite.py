import sqlite3

DATABASE_NAME = 'mydatabase.db'
TABLE_NAME = 'users'

def create_table():
    """Crea la tabella nel database SQLite se non esiste."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            età INTEGER,
            città TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Tabella '{TABLE_NAME}' creata (se non esisteva) nel database '{DATABASE_NAME}'.")

def write_to_sqlite(data):
    """Salva una lista di dizionari nel database SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    for item in data:
        cursor.execute(f'''
            INSERT INTO {TABLE_NAME} (nome, età, città)
            VALUES (?, ?, ?)
        ''', (item['nome'], item.get('età'), item.get('città')))
    conn.commit()
    conn.close()
    print(f"{len(data)} record scritti con successo nella tabella '{TABLE_NAME}'.")

if __name__ == '__main__':
    create_table()
    data_to_save = [
        {'nome': 'Alice', 'età': 30, 'città': 'Milano'},
        {'nome': 'Bob', 'età': 25, 'città': 'Roma'},
        {'nome': 'Charlie', 'età': 35, 'città': 'Napoli'}
    ]
    write_to_sqlite(data_to_save)
