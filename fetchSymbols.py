import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def fetch_stocks(api_key):
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Filter based on exchange and price
        filtered_stocks = [
            stock for stock in data 
            if (stock['exchange'] == 'New York Stock Exchange Arca' or 
                stock['exchange'] == 'NASDAQ Global Market') and 
                float(stock.get('price') or 0) > 5  # Modified line
        ]
        return filtered_stocks
    else:
        print("Failed to fetch data")
        return []

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

# Use your API key here
api_key = os.getenv('FM_API_KEY')
filtered_stocks = fetch_stocks(api_key)

print(f"Found {len(filtered_stocks)} stocks on NYSE Arca or NASDAQ Global Market with price > $5.")
# Print the first 10 symbols and prices as a sample
for stock in filtered_stocks[:10]:
    print(f"Symbol: {stock['symbol']}, Price: {stock['price']}")

# Save the filtered stocks to a JSON file
save_to_json(filtered_stocks, 'filtered_stocks.json')

