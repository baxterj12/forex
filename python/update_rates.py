import re, requests
import psycopg2
import time
from dotenv import load_dotenv
import os

load_dotenv()

connection = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = connection.cursor()

def postRates():
    country="USD"
    api_key = os.getenv("API_KEY")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{country}" #FINAL CODE CHANGES RATE CONVERTER
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        data = response.json()  # Parse the JSON response
        conversion_rates = data['conversion_rates']
        current_time = time.strftime('%Y-%m-%d')  # Get the current date
        for target_currency, exchange_rate in conversion_rates.items():
            cursor.execute("INSERT INTO exchange_rates (date, base_currency, target_currency, exchange_rate) VALUES (%s, %s, %s, %s)", (current_time, country, target_currency, exchange_rate))
        connection.commit()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    postRates()