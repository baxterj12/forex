import re, requests
import psycopg2
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = connection.cursor()

def postRates():
    """
    Fetches the latest exchange rates for a list of country codes and posts them to the database.
    This is a cron job run daily at 10am to fetch up to date exchange rates and push them to PostgreSQL database.
    Each row contains the date, base currency, target currency, and current exchange rate.
    """
    country_codes = [
    "AED", "AFN", "ALL", "AMD", "ANG", "AOA", "ARS", "AUD", "AWG", "AZN", "BAM", "BBD", "BDT", "BGN", "BHD", "BIF",
    "BMD", "BND", "BOB", "BRL", "BSD", "BTN", "BWP", "BYN", "BZD", "CAD", "CDF", "CHF", "CLP", "CNY", "COP", "CRC",
    "CUP", "CVE", "CZK", "DJF", "DKK", "DOP", "DZD", "EGP", "ERN", "ETB", "EUR", "FJD", "FKP", "FOK", "GBP", "GEL",
    "GGP", "GHS", "GIP", "GMD", "GNF", "GTQ", "GYD", "HKD", "HNL", "HRK", "HTG", "HUF", "IDR", "ILS", "IMP", "INR",
    "IQD", "IRR", "ISK", "JEP", "JMD", "JOD", "JPY", "KES", "KGS", "KHR", "KID", "KMF", "KRW", "KWD", "KYD", "KZT",
    "LAK", "LBP", "LKR", "LRD", "LSL", "LYD", "MAD", "MDL", "MGA", "MKD", "MMK", "MNT", "MOP", "MRU", "MUR", "MVR",
    "MWK", "MXN", "MYR", "MZN", "NAD", "NGN", "NIO", "NOK", "NPR", "NZD", "OMR", "PAB", "PEN", "PGK", "PHP", "PKR",
    "PLN", "PYG", "QAR", "RON", "RSD", "RUB", "RWF", "SAR", "SBD", "SCR", "SDG", "SEK", "SGD", "SHP", "SLE", "SLL",
    "SOS", "SRD", "SSP", "STN", "SYP", "SZL", "THB", "TJS", "TMT", "TND", "TOP", "TRY", "TTD", "TVD", "TWD", "TZS",
    "UAH", "UGX", "USD", "UYU", "UZS", "VES", "VND", "VUV", "WST", "XAF", "XCD", "XDR", "XOF", "XPF", "YER", "ZAR",
    "ZMW", "ZWL"
    ]
    api_key = os.getenv("API_KEY")
    for country in country_codes:
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