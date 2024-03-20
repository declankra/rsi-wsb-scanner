import pandas as pd
import yfinance as yf

def calculate_stoch(stock_symbol, threshold_value):
    # Download historical data for the stock
    data = yf.download(stock_symbol, period="6mo")

    # Calculate the Stochastic Oscillator
    low_min = data['Low'].rolling(window=14).min()
    high_max = data['High'].rolling(window=14).max()

    data['%K'] = (data['Close'] - low_min) * 100 / (high_max - low_min)
    data['%D'] = data['%K'].rolling(window=3).mean()
    data['slow_%D'] = data['%D'].rolling(window=3).mean()

    # Get the last values
    fast_d = data['%D'].iloc[-1]
    slow_d = data['slow_%D'].iloc[-1]

    # Determine overbought signals
    overbought_signal_fast_slow = 1 if fast_d < slow_d else 0
    overbought_signal_slow_threshold = ((slow_d-threshold_value) / threshold_value) * 100

    # Prepare DataFrame for output
    output_df = pd.DataFrame({
        "Stock Symbol": [stock_symbol],
        "Fast %D": [fast_d],
        "Slow %D": [slow_d],
        "Overbought Signal (Fast vs Slow)": [overbought_signal_fast_slow],
        "Overbought Signal (Slow > Threshold)": [overbought_signal_slow_threshold]
    })

    return output_df

# Variables defined within the script
stock_symbol = "SDRC"  # Example stock symbol
threshold_value = 75   # Example threshold value

# Calculate Stoch and print DataFrame
stoch_df = calculate_stoch(stock_symbol, threshold_value)
print(stoch_df)
