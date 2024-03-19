import json
import yfinance as yf
import pandas as pd

def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)
    avg_gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    avg_loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def fetch_and_calculate_rsi(symbols, threshold, period=14):
    rsi_values = {}
    for symbol in symbols:
        data = yf.download(symbol, period="1mo")
        if not data.empty:
            rsi = calculate_rsi(data, period)
            rsi_last = rsi.iloc[-1]
            if rsi_last > threshold:  # Check if RSI is above the threshold
                rsi_values[symbol] = rsi_last
        else:
            rsi_values[symbol] = None
    return rsi_values

def read_symbols_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        symbols = [item['symbol'] for item in data]
    return symbols


# Example usage
file_path = '/Users/macbook/Code/rsi-wsb-scanner/technical/yf/screened_stocks.json'
threshold = 89 # rsi criteria
symbols = read_symbols_from_json(file_path)
rsi_values = fetch_and_calculate_rsi(symbols, threshold)
print(rsi_values)

