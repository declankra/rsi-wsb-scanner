import praw
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize PRAW with your Reddit app credentials
reddit = praw.Reddit(client_id= os.getenv('REDDIT_CLIENT'),
                     client_secret= os.getenv('REDDIT_SECRET'),
                     user_agent=os.getenv('REDDIT_USER_AGENT'))

def fetch_title_mentions(ticker, days_ago, subreddit="wallstreetbets", limit=None):
    """Fetch the number of mentions for the given ticker and time frame."""
    after_timestamp = int((datetime.now() - timedelta(days=days_ago)).timestamp())
    mentions = 0
    
    for submission in reddit.subreddit(subreddit).new(limit=limit):
        if submission.created_utc < after_timestamp:
            break
        if ticker.lower() in submission.title.lower():
            mentions += 1
            
    return mentions

def calculate_relative_strength(ticker):
    """Calculate the relative strength of mentions for the given ticker."""
    # Average mentions in the last 30 days
    mentions_30d = fetch_title_mentions(ticker, 30)
    average_mentions_30d = mentions_30d / 30
    
    # Total mentions in the past 48 hours
    mentions_48h = fetch_title_mentions(ticker, 2)
    
    # Calculate relative strength
    if average_mentions_30d > 0:
        relative_strength = mentions_48h / average_mentions_30d
    else:
        relative_strength = 0  # To avoid division by zero
    
    return relative_strength

# Example usage
ticker = "apple"  # Replace with the actual ticker
relative_strength = calculate_relative_strength(ticker)
print(f"Relative Strength for {ticker} in Title: {relative_strength}")
