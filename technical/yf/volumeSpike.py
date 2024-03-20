import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(symbol):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=365)  # Approximation for 52 weeks
    data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
    return data

def calculate_volumes(data, days):
    volumes = data['Volume'].tail(days)
    average_volume = volumes.mean()
    return average_volume

def volume_spike(symbol):
    data = fetch_stock_data(symbol)
    recent_volume = data['Volume'].iloc[-1]

    periods = {
        "52 weeks": 365,
        "60 days": 60,
        "30 days": 30,
        "10 days": 10,
        "5 days": 5
    }

    results = {
        "most_recent_day_volume": recent_volume
    }

    for period, days in periods.items():
        avg_volume = calculate_volumes(data, days)
        percent_diff = ((recent_volume - avg_volume) / avg_volume) * 100
        results[f"avg_volume_{period}"] = avg_volume
        results[f"percent_diff_{period}"] = percent_diff

    return results

# Example usage
if __name__ == "__main__":
    symbol = "AAPL"  # Replace with any stock symbol
    results = volume_spike(symbol)
    print(results)
