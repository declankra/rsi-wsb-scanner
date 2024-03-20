import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_bollinger_band_percentage_recent(ticker, end_date):
    # Calculate start date as 3 months prior to the end date
    start_date = end_date - relativedelta(months=3)
    
    # Fetch historical stock data
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    
    # Define function to calculate Bollinger Bands
    def add_bollinger_bands(data, window):
        sma = data['Close'].rolling(window=window).mean()
        std = data['Close'].rolling(window=window).std()
        
        upper_band = sma + (std * 2)
        lower_band = sma - (std * 2)
        
        percent_above_upper = (data['Close'] - upper_band) / upper_band * 100
        
        return sma, upper_band, lower_band, percent_above_upper
    
    # Calculate for 10-day SMA and 20-day SMA
    stock_data['SMA_10'], stock_data['Upper_Band_10'], stock_data['Lower_Band_10'], \
    stock_data['Percent_Above_Upper_10'] = add_bollinger_bands(stock_data, 10)
    stock_data['SMA_20'], stock_data['Upper_Band_20'], stock_data['Lower_Band_20'], \
    stock_data['Percent_Above_Upper_20'] = add_bollinger_bands(stock_data, 20)
    
    # Select the most recent date's data
    most_recent_data = stock_data.iloc[-1:]
    
    return most_recent_data[['Close', 'Upper_Band_10', 'Percent_Above_Upper_10', 'Upper_Band_20', 'Percent_Above_Upper_20']]

# Example usage
ticker = "HAS"
end_date = datetime.today()

recent_data = calculate_bollinger_band_percentage_recent(ticker, end_date)

# Display the data for the most recent date
print(recent_data)
