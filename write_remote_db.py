import psycopg2

# Dettagli di connessione al database PostgreSQL
DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
TABLE_NAME = 'users'

def create_table_remote():
    """Crea la tabella nel database PostgreSQL se non esiste."""
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id SERIAL PRIMARY KEY,
                nome VARCHAR(255) NOT NULL,
                età INTEGER,
                città VARCHAR(255)
            )
        ''')
        conn.commit()
        print(f"Tabella '{TABLE_NAME}' creata (se non esisteva) nel database PostgreSQL '{DB_NAME}' su '{DB_HOST}'.")
    except psycopg2.Error as e:
        print(f"Errore durante la creazione della tabella PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()

def write_to_remote_db(data):
    """Salva una lista di dizionari nel database PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        for item in data:
            cursor.execute(f'''
                INSERT INTO {TABLE_NAME} (nome, età, città)
                VALUES (%s, %s, %s)
            ''', (item['nome'], item.get('età'), item.get('città')))
        conn.commit()
        print(f"{len(data)} record scritti con successo nella tabella '{TABLE_NAME}' nel database PostgreSQL.")
    except psycopg2.Error as e:
        print(f"Errore durante il salvataggio nel database PostgreSQL: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    # Assicurati di aver installato la libreria psycopg2: pip install psycopg2-binary
    # E di aver configurato correttamente le credenziali di connessione

    # Sostituisci con le tue informazioni di connessione al database
    DB_HOST = "localhost"  # Esempio: potrebbe essere l'IP del server remoto
    DB_NAME = "your_database"
    DB_USER = "your_username"
    DB_PASSWORD = "your_password"

    create_table_remote()
    data_to_save = [
        {'nome': 'Alice', 'età': 30, 'città': 'Milano'},
        {'nome': 'Bob', 'età': 25, 'città': 'Roma'},
        {'nome': 'Charlie', 'età': 35, 'città': 'Napoli'}
    ]
    write_to_remote_db(data_to_save)
