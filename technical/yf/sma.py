import yfinance as yf
import pandas as pd

def calculate_sma_percentages(ticker_symbol):
    # Download historical data for the given ticker
    data = yf.download(ticker_symbol, period="1mo")
    
    # Calculate the SMA values for 20, 10, and 5 days
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_10'] = data['Close'].rolling(window=10).mean()
    data['SMA_5'] = data['Close'].rolling(window=5).mean()
    
    # Extract the most recent row of data
    latest_data = data.iloc[-1]
    close_price = latest_data['Close']
    
    # Calculate the percentages
    sma_20_percent = ((close_price - latest_data['SMA_20']) / latest_data['SMA_20']) * 100
    sma_10_percent = ((close_price - latest_data['SMA_10']) / latest_data['SMA_10']) * 100
    sma_5_percent = ((close_price - latest_data['SMA_5']) / latest_data['SMA_5']) * 100
    
    # Print the SMA values and the corresponding percentages
    print(f"Stock: {ticker_symbol}")
    print(f"Closing Price: {close_price:.2f}")
    print(f"20-day SMA: {latest_data['SMA_20']:.2f}, Percent Above/Below: {sma_20_percent:.2f}%")
    print(f"10-day SMA: {latest_data['SMA_10']:.2f}, Percent Above/Below: {sma_10_percent:.2f}%")
    print(f"5-day SMA: {latest_data['SMA_5']:.2f}, Percent Above/Below: {sma_5_percent:.2f}%")

# Example usage
ticker = "HAS"  # Change this to the ticker you're interested in
calculate_sma_percentages(ticker)
