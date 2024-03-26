

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)  # Approximation for 52 weeks
    data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    return data

symbols = {"SDRC", "EGO", "SG", "FIHL", "HAS", "SMCI", "PANW"}

for symbol in symbols:
    data = fetch_stock_data(symbol)
    filename = f"{symbol}.csv"
    data.to_csv(filename)
    print(f"Data for {symbol} saved to {filename}.")
