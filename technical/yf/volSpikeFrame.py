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

    periods = [365, 60, 30, 10, 5]  # Representing 52 weeks, 60, 30, 10, and 5 days

    # Initialize an empty DataFrame to store results
    results_df = pd.DataFrame(columns=['Period', 'Average_Volume', 'Most_Recent_Volume', 'Percent_Difference'])

    for days in periods:
        avg_volume = calculate_volumes(data, days)
        percent_diff = ((recent_volume - avg_volume) / avg_volume) * 100

        # Convert 365 days to '52 weeks' for readability
        period_name = f'{days} days' if days != 365 else '52 weeks'
        
        # Properly append row to DataFrame
        results_df = results_df._append({
            'Period': period_name,
            'Average_Volume': avg_volume,
            'Most_Recent_Volume': recent_volume,
            'Percent_Difference': percent_diff
        }, ignore_index=True)

    return results_df

# Example usage
if __name__ == "__main__":
    symbol = "EGO"  # Replace with any stock symbol
    results_df = volume_spike(symbol)
    print(results_df)
