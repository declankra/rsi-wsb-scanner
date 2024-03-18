import praw
from datetime import datetime, timedelta

# Initialize PRAW with your Reddit app credentials
reddit = praw.Reddit(client_id='QyyiKi73QvFJqi_nX9ALQg',
                     client_secret='njKqQqY8r2JEn_V4SuWrg1uNn2FJig',
                     user_agent='fetchWSB')

def fetch_mentions(ticker, days_ago, subreddit="wallstreetbets", limit=None):
    """Fetch the number of mentions for the given ticker and time frame."""
    after_timestamp = int((datetime.now() - timedelta(days=days_ago)).timestamp())
    mentions = 0
    
    for submission in reddit.subreddit(subreddit).new(limit=limit):
        if submission.created_utc < after_timestamp:
            break
        # Check if the ticker is mentioned in either the title or the body of the submission
        if ticker.lower() in submission.title.lower() or ticker.lower() in submission.selftext.lower():
            mentions += 1
            
    return mentions

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
ticker = "smci"  # Replace with the actual ticker
relative_strength = calculate_relative_strength(ticker)
print(f"Relative Strength for {ticker} in Title or Body: {relative_strength}")
