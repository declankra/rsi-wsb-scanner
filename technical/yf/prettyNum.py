import yfinance as yf
import pandas as pd

def is_close_to_pretty_number(symbol):
    # Fetch data
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")
    close_price = hist['Close'].iloc[-1]

    # Increments and tolerances
    increments = [100, 50, 25, 10]
    tolerances = [10, 5, 3, 1.5]

    results = {}

    # Calculate and check against tolerances
    for increment, tolerance in zip(increments, tolerances):
        closeness = close_price % increment
        is_close = int(closeness < tolerance or (increment - closeness) < tolerance)
        results[f"Close to {increment}?"] = is_close

    return results

# Input
symbol = "AAPL" # Example: Use the symbol for the stock you're interested in

# Output
results = is_close_to_pretty_number(symbol)
for key, value in results.items():
    print(f"{key}: {'Yes' if value else 'No'}")
