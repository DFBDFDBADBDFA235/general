import psycopg2

# Dettagli di connessione al database PostgreSQL
DB_HOST = "your_db_host"
DB_NAME = "your_db_name"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"
TABLE_NAME = 'users'

def read_from_remote_db():
    """Legge tutti i dati dalla tabella nel database PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {TABLE_NAME}')
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] # Ottieni i nomi delle colonne
        print(f"Dati letti con successo dalla tabella '{TABLE_NAME}' nel database PostgreSQL.")
        return [dict(zip(columns, row)) for row in rows]
    except psycopg2.Error as e:
        print(f"Errore durante la lettura dal database PostgreSQL: {e}")
        return []
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

    loaded_data = read_from_remote_db()
    if loaded_data:
        print("Dati caricati da PostgreSQL:")
        for row in loaded_data:
            print(row)
