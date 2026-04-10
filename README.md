# NBP Exchange Rates Pipeline

## PL
Pipeline pobierający kursy walut z API Narodowego Banku Polskiego 
i zapisujący je do bazy danych PostgreSQL.

### Funkcjonalności
- Pobieranie danych historycznych z podaniem zakresu dat
- Pobieranie danych przyrostowo od ostatniej daty w bazie
- Automatyczny podział na chunki (limit API: 93 dni)
- Zabezpieczenie przed duplikatami (UNIQUE constraint na code + effective_date)
- Obsługa błędów i logowanie


### Technologie
- Python (requests, pandas, psycopg2, argparse)
- PostgreSQL
- dbt
- GitHub Actions (pokazowo, baza skonfigurowana lokalnie)

## Architektura / Architecture

raw_exchange_rates (PostgreSQL)
    ↓ dbt
stg_nbp_rates (staging - oczyszczone dane)
    ↓ dbt
dim_currency (wymiar walut)
mart_monthly_avg (średnia miesięczna per waluta)
mart_mom_change (zmiana miesiąc do miesiąca)

* Warstwa staging - oczyszczenie i ujednolicenie danych
* dim_currency - wymiar z unikalnymi walutami
* mart_monthly_avg - średnia miesięczna kursu per waluta
* mart_mom_change - zmiana kursu miesiąc do miesiąca (MoM)

### Uruchomienie

Zainstaluj zależności:
pip install -r requirements.txt

Stwórz plik .env na podstawie .env.example i uzupełnij dane do bazy.

Pobierz dane historyczne:
py insert_records.py --start_date 2024-01-01 --end_date 2024-12-31

Pobierz dane przyrostowo:
py insert_records.py

---

## EN
Pipeline fetching exchange rates from the National Bank of Poland API 
and storing them in a PostgreSQL database.

### Features
- Historical data ingestion with custom date range
- Incremental data loading from last available date in database
- Automatic chunking due to 93-day API limit
- Duplicate prevention (UNIQUE constraint on code + effective_date)
- Error handling

### Tech Stack
- Python (requests, pandas, psycopg2, argparse)
- PostgreSQL
- dbt
- GitHub Actions (only preview, working on localhost)

* Staging layer - data cleaning and standardization
* dim_currency - dimension table with unique currencies
* mart_monthly_avg - monthly average exchange rate per currency
* mart_mom_change - month-over-month exchange rate change


### How to run

Install dependencies:
pip install -r requirements.txt

Create .env file based on .env.example and fill in your database credentials.

Historical load:
py insert_records.py --start_date 2024-01-01 --end_date 2024-12-31

Incremental load:
py insert_records.py
