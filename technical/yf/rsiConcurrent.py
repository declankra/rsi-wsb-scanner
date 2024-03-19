import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def calculate_rsi(data, period=14):
    delta = data['Close'].diff(1)
    avg_gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    avg_loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def fetch_stock_data(symbol, period="1mo"):
    # Ensure symbol is a string
    symbol_str = str(symbol)
    data = yf.download(symbol_str, period=period)
    return symbol, data


def fetch_and_calculate_rsi(symbols, threshold, period=14, max_workers=50):
    rsi_values = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Initiate all fetch requests in parallel
        future_to_symbol = {executor.submit(fetch_stock_data, symbol, period): symbol for symbol in symbols}
        
        for future in as_completed(future_to_symbol):
            symbol = future_to_symbol[future]
            try:
                _, data = future.result()
                if not data.empty:
                    rsi = calculate_rsi(data, period)
                    rsi_last = rsi.iloc[-1]
                    if rsi_last > threshold:  # Check if RSI is above the threshold
                        rsi_values[symbol] = rsi_last
            except Exception as e:
                print(f"Error fetching data for {symbol}: {e}")
                rsi_values[symbol] = None
                
    return rsi_values

# Example usage
symbols = ['AAPL', 'MSFT', 'GOOGL', 'BNIX']  # Add your stock symbols here
threshold = 89  # RSI criteria
rsi_values = fetch_and_calculate_rsi(symbols, threshold)
print(rsi_values)
