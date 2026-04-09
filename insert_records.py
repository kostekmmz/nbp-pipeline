from api_request import parse_data, fetch_data
import psycopg2
import argparse
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_db():
    print("Łączę się z bazą danych..")
    try:
       conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
       return conn
    except psycopg2.Error as e:
        print(f"Wystąpił błąd podczas łączenia z bazą danych {e}")
        raise


def create_table(conn):
    print("Tworzenie tabeli jeżeli nie istnieje...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE SCHEMA IF NOT EXISTS exch_rates;
        CREATE TABLE IF NOT EXISTS exch_rates.raw_exchange_rates (
            id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
            currency VARCHAR(100),
            code VARCHAR(10),
            mid DECIMAL(10,6),
            effective_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
	);
    """)
        conn.commit()
        print("Tabela utworzona.")
    except psycopg2.Error as e:
        print(f"Wystąpił błąd podczas tworzenia tabeli {e}")
        raise

def insert_data(conn, df):
    
    print("Wgrywanie danych do tabeli")
    try:
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT INTO exch_rates.raw_exchange_rates(
                currency,
                code,
                mid,
                effective_date)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (code, effective_date) DO NOTHING 
                """,list(  ###dodajemy on conflict do nothing żeby nie zamykało połączenia z bazą, ale nie wgrywało dubli do środka
                    zip(
                    df['currency'],
                    df['code'],
                    df['mid'],
                    df['effectiveDate']
                )))
        conn.commit()
        print ("Dane wgrane prawidłowo.")
    except psycopg2.Error as e:
        print(f"Wystąpił błąd przy wgrywaniu danych {e}")
        raise

def get_last_date(conn):
    print("Pobieram ostatnią datę z bazy")
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(effective_date) FROM exch_rates.raw_exchange_rates")
        wynik = cursor.fetchone()
        if wynik[0] is None:
            wynik = date(2026,4,1)
        else:
            wynik = wynik[0] + timedelta(days=1)
    except Exception as e:
        print(f"Wystąpił błąd {e}")
        raise
    return wynik

def generate_date_chunks(start_date, end_date, chunk_size=93):
    chunks = []
    current = start_date
    while current < end_date:
        chunk_end = min(current + timedelta(days=chunk_size), end_date) # min is taking date +93 days or end_date depends which is earlier
        chunks.append((current, chunk_end))
        current = chunk_end + timedelta(days=1)
    return chunks

def main():
    parser = argparse.ArgumentParser()
    conn = connect_to_db()
    parser.add_argument('--start_date', required=False)
    parser.add_argument('--end_date', required=False)
    args = parser.parse_args()
    #start_date = get_last_date(conn)
    #chunks = generate_date_chunks
    if args.start_date is None:
        start_date = get_last_date(conn)
        end_date = date.today() - timedelta(days=1)
    else:
        start_date = args.start_date
        end_date = args.end_date
   
    try:
        chunks = generate_date_chunks(start_date, end_date)
        for chunk_start, chunk_end in chunks:
            dane = fetch_data(chunk_start, chunk_end)
            df = parse_data(dane)
            insert_data(conn,df)
    except Exception as e:
        print(f"Wystąpił błąd {e}")
        if 'conn' in locals() and conn:
            conn.close()
            print("Połączenie z bazą zostało zamknięte.")

if __name__ == "__main__":
    main()





