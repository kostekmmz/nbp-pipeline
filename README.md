# NBP Exchange Rates Pipeline

Pipeline pobierający kursy walut z API Narodowego Banku Polskiego i zapisujący je do bazy danych PostgreSQL.

*Pipeline fetching exchange rates from the National Bank of Poland API and storing them in a PostgreSQL database.*

---

## Architektura / Architecture
raw_exchange_rates (PostgreSQL)
↓ dbt
stg_nbp_rates (staging)
↓ dbt
├── dim_currency
├── mart_monthly_avg
└── mart_mom_change
---

## Funkcjonalności / Features

| PL | EN |
|---|---|
| Pobieranie danych historycznych z podaniem zakresu dat | Historical data ingestion with custom date range |
| Pobieranie danych przyrostowo od ostatniej daty w bazie | Incremental data loading from last available date |
| Automatyczny podział na chunki (limit API: 93 dni) | Automatic chunking due to 93-day API limit |
| Zabezpieczenie przed duplikatami (UNIQUE constraint) | Duplicate prevention (UNIQUE constraint) |
| Obsługa błędów | Error handling |

---

## Modele dbt / dbt Models

| Model | Opis / Description |
|---|---|
| `stg_nbp_rates` | Oczyszczone dane / Cleaned raw data |
| `dim_currency` | Wymiar walut / Currency dimension |
| `mart_monthly_avg` | Średnia miesięczna / Monthly average rate |
| `mart_mom_change` | Zmiana MoM / Month-over-month change |

---

## Tech Stack

- Python (`requests`, `pandas`, `psycopg2`, `argparse`, `python-dotenv`)
- PostgreSQL
- dbt (dbt-postgres)
- GitHub Actions *(demo — baza skonfigurowana lokalnie / localhost only)*

---

## Uruchomienie / How to run

**1. Zainstaluj zależności / Install dependencies**
```bash
pip install -r requirements.txt
```

**2. Skonfiguruj zmienne środowiskowe / Configure environment**
```bash
cp .env.example .env
# uzupełnij dane do bazy / fill in your database credentials
```

**3. Pobierz dane historyczne / Historical load**
```bash
py insert_records.py --start_date 2024-01-01 --end_date 2024-12-31
```

**4. Pobierz dane przyrostowo / Incremental load**
```bash
py insert_records.py
```

**5. Uruchom transformacje dbt / Run dbt transformations**
```bash
cd nbp_dbt
dbt run
```
