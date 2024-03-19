import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_symbols_for_exchange(api_key, exchange):
    # Assuming this function now fetches detailed data including price, volume, and marketCap
    url = f"https://financialmodelingprep.com/api/v3/symbol/{exchange.upper()}?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch symbols for {exchange}")
        return []

def filter_symbols(symbols):
    # Filter symbols with safety checks for None values
    filtered = [
        symbol for symbol in symbols
        if (symbol.get('price') or 0) > 5 and (symbol.get('volume') or 0) > 500000 and (symbol.get('marketCap') or 0) > 300000000
    ]
    return filtered


def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Use your API key here
api_key = os.getenv('FM_API_KEY')
exchanges = ['nyse', 'nasdaq'] ## removed amex
all_filtered_symbols = []

for exchange in exchanges:
    symbols = fetch_symbols_for_exchange(api_key, exchange)  # fetch_symbols_for_exchange should already be defined
    filtered_symbols = filter_symbols(symbols)  # Now uses the updated filtering criteria
    all_filtered_symbols.extend(filtered_symbols)
    print(f"Found {len(filtered_symbols)} filtered symbols on {exchange}.")

print(f"Total filtered symbols found across all exchanges: {len(all_filtered_symbols)}")

# Optionally, print the symbols of the first 10 stocks as a sample
for symbol in all_filtered_symbols[:10]:
    print(symbol['symbol'])

# Save the combined list of filtered symbols to a JSON file
save_to_json(all_filtered_symbols, 'filtered_exchange_symbols.json')

