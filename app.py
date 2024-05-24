from flask import Flask, render_template, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.static_folder = 'static'

# Constants
HOLDER_API_URL = "https://suiscan.xyz/api/sui-backend/mainnet/api/coins/0xa8816d3a6e3136e86bc2873b1f94a15cadc8af2703c075f2d546c2ae367f4df9::ocean::OCEAN/holders?page=0&sortBy=AMOUNT&orderBy=DESC&searchStr=&size=10000"
INFO_API_URL = "https://suiscan.xyz/api/sui-backend/mainnet/api/coins/0xa8816d3a6e3136e86bc2873b1f94a15cadc8af2703c075f2d546c2ae367f4df9::ocean::OCEAN"

def get_holders_data():
    response = requests.get(HOLDER_API_URL)
    info = requests.get(INFO_API_URL)
    if response.status_code == 200:
        return response.json().get("content", []), info.json().get("tokenPrice", 0), info.json().get("holders", 0)
    else:
        print(f"Failed to retrieve data")
        return []

def calculate_token_holding():
    top_10000_token_holding = 0.0
    holders, price, total_current_holder = get_holders_data()
    total_current_holder = "{:,.0f}".format(total_current_holder)
    top_wallets = {}
    for i, holder in enumerate(holders):
        if i < 10:
            address = holder['address']
            amount = "{:,.2f}".format(round(holder['amount'],4))
            top_wallets[i] = {}
            top_wallets[i][address] = amount
        top_10000_token_holding += float(holder['amount'])
    return top_10000_token_holding, top_wallets, price, total_current_holder

@app.route('/token_analysis', methods=['GET'])
def token_holding():
    top_10000_token_holding, top_wallets, price, total_current_holder = calculate_token_holding()
    formatted_total = "{:,.2f}".format(round(top_10000_token_holding,2))
    return jsonify(top_10000_token_holding=formatted_total, top_wallets = top_wallets, price = round(price,5), total_current_holder = total_current_holder)

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
