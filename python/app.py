from flask import Flask, jsonify, request
from flask_cors import CORS
import re, requests
import psycopg2
import time

app = Flask(__name__)
CORS(app)

connection = psycopg2.connect(
    database="forex",
    user="postgres",
    password="Fb842638",
    host="localhost",
    port="5432"
)
cursor = connection.cursor()


#EXCHANGE RATE INFO
@app.route('/get_exrates', methods=['GET'])
def get_exrates ():
    try:
        print("in try")
        rates = {}
        cursor.execute("SELECT target_currency, exchange_rate FROM exchange_rates ORDER BY created_at DESC LIMIT 162;")
        print("after select")
        rows = cursor.fetchall()
        for k,v in rows: 
            rates[k]=float(v)
        return (rates)
    except psycopg2.Error as e:
        print(f"Database error: {str(e)}")  # Log the error for debugging
        return jsonify({"error": f"Database error: {str(e)}"}), 500

#Post rates to database

def makeTrade():

    cur_from = request.args.get('from')
    to = request.args.get('to')
    amount = request.args.get('amount')

    

'''def postRates():
    country = request.args.get('country', 'USD')

    if not re.match(r'^[A-Z]{3}$', country):
        raise ValueError("Country code must be 3 uppercase letters")
    
    api_key = 'becb6fe99bfa76b8404acc49'
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
'''

@app.route('/trades', methods=['GET'])
def viewTrades ():
    return None

@app.route('/getAllBalances', methods=['GET'])
def getAllBalances():
    balances = {}
    cursor.execute("SELECT * FROM accounts;")
    rows = cursor.fetchall()
    for k,v in rows: 
        balances[k]=float(v)
    return (balances)

if __name__ == '__main__':
    app.run(debug=True)
