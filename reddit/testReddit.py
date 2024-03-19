from pmaw import PushshiftAPI
api = PushshiftAPI()
from datetime import datetime, timedelta

def get_date_str(days_ago):
    """Return the date in 'YYYY-MM-DD' format for the given days ago."""
    target_date = datetime.now() - timedelta(days=days_ago)
    return target_date.strftime('%Y-%m-%d')

def fetch_mentions(ticker, days_ago, size=500):
    """Fetch the number of mentions for the given ticker and time frame."""
    ####after_date_calc = get_date_str(days_ago)
    posts = api.search_submissions(q = ticker, subreddit="wallstreetbets", limit = size)
    return len(posts)

def calculate_relative_strength(ticker):
    """Calculate the relative strength of mentions for the given ticker."""
    # Average mentions in the last 30 days
    mentions_30d = fetch_mentions(ticker, 30)
    average_mentions_30d = mentions_30d / 30
    
    # Total mentions in the past 48 hours
    mentions_48h = fetch_mentions(ticker, 2)
    
    # Calculate relative strength
    if average_mentions_30d > 0:
        relative_strength = mentions_48h / average_mentions_30d
    else:
        relative_strength = 0  # To avoid division by zero
    
    return relative_strength

# Example usage
ticker = "AAPL"  # Replace with the actual ticker
relative_strength = calculate_relative_strength(ticker)
print(f"Relative Strength for {ticker}: {relative_strength}")
