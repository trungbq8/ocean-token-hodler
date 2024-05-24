from flask import Flask, render_template, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

# Constants
BASE_URL = "https://suiscan.xyz/api/sui-backend/mainnet/api/coins/0xa8816d3a6e3136e86bc2873b1f94a15cadc8af2703c075f2d546c2ae367f4df9::ocean::OCEAN/holders?page=0&sortBy=AMOUNT&orderBy=DESC&searchStr=&size=10000"

def get_holders_data():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        return response.json().get("content", [])
    else:
        print(f"Failed to retrieve data")
        return []

def calculate_token_holding():
    token_holding = 0.0
    holders = get_holders_data()
    for holder in holders:
        token_holding += float(holder['amount'])
    return token_holding

@app.route('/token_holding', methods=['GET'])
def token_holding():
    total = calculate_token_holding()
    formatted_total = "{:,.2f}".format(round(total,2))
    return jsonify(token_holding=formatted_total)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)