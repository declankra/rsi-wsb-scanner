import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_filtered_stocks_for_exchange(api_key, exchange):
    url = "https://financialmodelingprep.com/api/v3/stock-screener"
    params = {
        'apikey': api_key,
        'marketCapMoreThan': 10000000,
        'priceMoreThan': 5,
        'volumeMoreThan': 1000,
        'isEtf': False,
        'isFund': False,
        'isActivelyTrading': 'true',
        'exchange': exchange
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for {exchange}")
        return []

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Use your API key here
api_key = os.getenv('FM_API_KEY')
exchanges = ['nyse', 'nasdaq', 'amex']
all_filtered_stocks = []

for exchange in exchanges:
    filtered_stocks = fetch_filtered_stocks_for_exchange(api_key, exchange)
    all_filtered_stocks.extend(filtered_stocks)
    print(f"Found {len(filtered_stocks)} stocks matching criteria on {exchange}.")

# Print the total number of stocks found across all exchanges
print(f"Total stocks found across all exchanges: {len(all_filtered_stocks)}")
# Optionally, print the symbols of the first 10 stocks as a sample
for stock in all_filtered_stocks[:10]:
    print(stock['symbol'])

# Save the combined list of filtered stocks to a JSON file
save_to_json(all_filtered_stocks, 'filtered_stocks.json')