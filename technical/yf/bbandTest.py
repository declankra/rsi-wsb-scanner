import yfinance as yf
import pandas as pd

# Step 1: Define the function to calculate Bollinger Bands and the percentage above the top band
def calculate_bollinger_band_percentage(ticker, start_date, end_date):
    # Fetch historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Calculate the 20-day moving average and standard deviation
    stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
    stock_data['STD_20'] = stock_data['Close'].rolling(window=20).std()
    
    # Calculate the Bollinger Bands
    stock_data['Upper_Band'] = stock_data['SMA_20'] + (stock_data['STD_20'] * 2)
    stock_data['Lower_Band'] = stock_data['SMA_20'] - (stock_data['STD_20'] * 2)
    
    # Calculate the percentage that the closing price is above the top Bollinger Band
    # If the closing price is below the upper band, the percentage is 0
    stock_data['Percent_Above_Upper'] = (stock_data['Close'] - stock_data['Upper_Band']) / stock_data['Upper_Band'] * 100
    stock_data['Percent_Above_Upper'] = stock_data['Percent_Above_Upper'].apply(lambda x: max(x, 0))
    
    return stock_data[['Close', 'Upper_Band', 'Percent_Above_Upper']]

# Step 2: Example usage
ticker = "HAS"  # Example: Apple Inc.
start_date = "2024-02-01"
end_date = "2024-03-19"

result = calculate_bollinger_band_percentage(ticker, start_date, end_date)

# Display the last few rows to see the most recent percentages
print(result.tail())
