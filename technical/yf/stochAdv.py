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
    last_k = data['%K'].iloc[-1]
    fast_d = data['%D'].iloc[-1]
    slow_d = data['slow_%D'].iloc[-1]

    # Determine overbought signal based on fast %D and slow %D
    overbought_signal_fast_slow = 1 if fast_d < slow_d else 0

    # Determine the better sell signal based on %K and slow %D threshold analysis
    overbought_indicator = "None"
    percent_over_threshold = 0.0

    if last_k > threshold_value or slow_d > threshold_value:
        if last_k - threshold_value > slow_d - threshold_value:
            overbought_indicator = "%K"
            percent_over_threshold = (last_k - threshold_value) / threshold_value * 100
        else:
            overbought_indicator = "slow %D"
            percent_over_threshold = (slow_d - threshold_value) / threshold_value * 100

    # Prepare DataFrame for output
    output_df = pd.DataFrame({
        "Stock Symbol": [stock_symbol],
        "Last %K": [last_k],
        "Fast %D": [fast_d],
        "Slow %D": [slow_d],
        "Overbought Signal (Fast vs Slow)": [overbought_signal_fast_slow],
        "Overbought Indicator": [overbought_indicator],
        "Percent Over Threshold": [percent_over_threshold]
    })

    return output_df

# Variables defined within the script
stock_symbol = "PLD"  # Example stock symbol
threshold_value = 80   # Adjusted example threshold value for demonstration

# Calculate Stoch and print DataFrame
stoch_df = calculate_stoch(stock_symbol, threshold_value)
print(stoch_df)
