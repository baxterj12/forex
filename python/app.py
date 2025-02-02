from flask import Flask, jsonify, request
from flask_cors import CORS
import re, requests
import psycopg2
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

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
