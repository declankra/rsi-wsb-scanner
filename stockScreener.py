import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_filtered_stocks(api_key):
    url = "https://financialmodelingprep.com/api/v3/stock-screener"
    params = {
        'apikey': api_key,
        'marketCapMoreThan': 10000000,
        'priceMoreThan': 5,
        'volumeMoreThan': 1000,
        'isEtf': 'false',
        'isFund': 'false',
        'isActivelyTrading': 'true',
        'exchange': 'nyse,nasdaq,amex'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return []

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Use your API key here
api_key = os.getenv('AV_API_KEY')
filtered_stocks = fetch_filtered_stocks(api_key)

print(f"Found {len(filtered_stocks)} stocks matching criteria.")
# Optionally, print the symbols of the first 10 stocks as a sample
for stock in filtered_stocks[:10]:
    print(stock['symbol'])

# Save the filtered stocks to a JSON file
save_to_json(filtered_stocks, 'filtered_stocks.json')
