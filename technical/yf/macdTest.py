import yfinance as yf
import pandas as pd
import numpy as np

# Fetch historical data
def fetch_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data

# Calculate MACD and Signal Line
def calculate_macd(data):
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    data['MACD'] = macd
    data['Signal Line'] = signal
    return data

# Identify Zero Cross Downwards
def zero_cross_downwards(data):
    data['Zero Cross Down'] = (data['MACD'] < 0) & (data['MACD'].shift(1) > 0)
    return data

# Identify potential overbought conditions
def detect_overbought_conditions(data):
    # Assuming divergence as price making new highs not followed by MACD
    highs = data['Close'] > data['Close'].rolling(window=14).max()
    macd_not_highs = data['MACD'] < data['MACD'].rolling(window=14).max()
    data['Potential Overbought'] = highs & macd_not_highs
    return data

# Main function to run the analysis
def main():
    stock_symbol = 'HAS'
    start_date = '2023-01-01'
    end_date = '2024-03-19'
    
    data = fetch_data(stock_symbol, start_date, end_date)
    data = calculate_macd(data)
    data = zero_cross_downwards(data)
    data = detect_overbought_conditions(data)
    
    overbought_signals = data[data['Potential Overbought'] | data['Zero Cross Down']]
    print(overbought_signals[['Close', 'MACD', 'Signal Line', 'Potential Overbought', 'Zero Cross Down']])

if __name__ == '__main__':
    main()
