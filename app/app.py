import psycopg2
from psycopg2 import sql
import time
"""
https://github.com/pgvector/pgvector/blob/master/README.md#docker
"""

def wait_for_db():
    retries = 5
    delay = 5  # secondi
    for attempt in range(retries):
        try:
            conn = psycopg2.connect(
                dbname='postgres',
                user='postgres',
                password='',
                host='postgresql',
                port='5432'
            )
            conn.close()
            print("Connessione al database stabilita.")
            return
        except Exception as e:
            print(f"Tentativo {attempt + 1} fallito: {e}")
            if attempt < retries - 1:
                print(f"Ritentando tra {delay} secondi...")
                time.sleep(delay)
            else:
                print("Impossibile connettersi al database dopo diversi tentativi.")
                raise


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='',
            host='postgresql',
            port='5432'
        )
        cur = conn.cursor()

        cur.execute("SELECT version();")
        db_version = cur.fetchone()
        print(f"Connesso al database. Versione del database: {db_version}")


        cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        cur.execute("CREATE TABLE IF NOT EXISTS items (id bigserial PRIMARY KEY, embedding vector(3));")
        cur.execute("INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');")
        cur.execute("SELECT * FROM items ORDER BY embedding <-> '[3,1,2]' LIMIT 5;")
        results = cur.fetchall()

        for row in results:
            print(f'result={row}')

        conn.commit()

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Errore durante la connessione al database: {e}")

if __name__ == "__main__":
    wait_for_db()
    connect_to_db()
