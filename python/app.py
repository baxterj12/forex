from flask import Flask, jsonify, request
from flask_cors import CORS
import re, requests
import psycopg2
import time
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Establish a connection to the PostgreSQL database
connection = psycopg2.connect(
    database=os.getenv("DATABASE_NAME"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    host=os.getenv("DATABASE_HOST"),
    port=os.getenv("DATABASE_PORT")
)
cursor = connection.cursor()

#EXCHANGE RATE INFO
@app.route('/get_exrates', methods=['GET'])
def get_exrates():
    """
    Retrieves exchange rates for a given country.
    
    Parameters:
    - country (str): The country code for which to retrieve exchange rates.
    
    Returns:
    - dict: A dictionary with target currencies as keys and the most recentexchange rates as values.
    """
    country = request.args.get('country')  # New parameter for country
    try:
        print("in try")
        print("country code " + country)
        rates = {}
        cursor.execute("SELECT target_currency, exchange_rate FROM exchange_rates WHERE base_currency = %s ORDER BY created_at DESC LIMIT 162;", (country,))
        #the above line selects only the most recent exchange rates, with LIMIT = 162 for the 162 available currencies on my API
        print("after select")
        rows = cursor.fetchall()
        for k, v in rows: 
            rates[k] = float(v)
            print(k)
            print(v)
        return jsonify(rates)  # Convert the dictionary to JSON before returning
    except psycopg2.Error as e:
        print(f"Database error: {str(e)}")  # Log the error for debugging
        return jsonify({"error": f"Database error: {str(e)}"}), 500

#Post rates to database
@app.route('/makeTrade', methods=['POST'])
def makeTrade():
    """
    In Progress
    Processes a trade by converting an amount from one currency to another.
    
    Parameters:
    - from (str): The source currency code.
    - to (str): The target currency code.
    - amount (float): The amount to be converted.
    - fee (float): The fee percentage for the conversion.
    
    Returns:
    - None: This function updates the database but does not return a value.
    """
    cur_from = request.args.get('from')
    to = request.args.get('to')
    amount = float(request.args.get('amount'))  # Convert to float
    fees = float(request.args.get("fee"))  # Convert to float
    cursor.execute("SELECT exchange_rate FROM exchange_rates WHERE base_currency = %s AND target_currency = %s ORDER BY created_at DESC LIMIT 1;", (cur_from, to))
    #selecting the most recent exchange rate between the two currencies
    rate = cursor.fetchall()
    newcurr_amount = amount * rate * (1 - (fees/100))
    cursor.execute("UPDATE accounts SET amount = amount - %s WHERE currency_code = %s;", (amount, cur_from))
    cursor.execute("UPDATE accounts SET amount = amount + %s WHERE currency_code = %s;", (newcurr_amount, to))
    #updating the accounts data table to remove the initial amount from the base currency and add the converted amount (minus fee) to the target currency

@app.route('/getAllBalances', methods=['GET'])
def getAllBalances():
    """
    Retrieves all account balances.
    
    Returns:
    - dict: A dictionary with currency codes as keys and their balances as values.
    """
    balances = {}
    cursor.execute("SELECT * FROM accounts;")
    rows = cursor.fetchall()
    for k,v in rows: 
        balances[k]=float(v)
    return jsonify(balances)  # Convert the dictionary to JSON before returning

if __name__ == '__main__':
    app.run(debug=True)
