import requests 
import pandas as pd
import json
from pandas import json_normalize


api_url = "https://api.nbp.pl/api/exchangerates/tables/A/{startDate}/{endDate}"

def fetch_data(start_date, end_date):
    print("Pobieranie danych z API:")
    url = api_url.format(startDate=start_date, endDate=end_date)
    print(f"Odpytuję url: {url}")
    try: 
        response = requests.get(url)
        response.raise_for_status()
        print("API otrzymało odpowiedź")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Wystąpił bład {e}")
        raise

def parse_data(dane):
    try:
        df =  pd.json_normalize(dane, record_path="rates", meta=["effectiveDate"])
        return df
    except Exception as e:
        print(f"Nie udało się sprasować danych {e}")
        raise


