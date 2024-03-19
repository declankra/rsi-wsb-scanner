from datetime import datetime, timedelta
import praw
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize PRAW with your Reddit app credentials
reddit = praw.Reddit(client_id= os.getenv('REDDIT_CLIENT'),
                     client_secret= os.getenv('REDDIT_SECRET'),
                     user_agent=os.getenv('REDDIT_USER_AGENT'))

def find_daily_discussion_comments(ticker, subreddit="wallstreetbets"):
    """Find the percentage of comments mentioning the ticker in the nearest past Daily Discussion thread."""
    today = datetime.utcnow()
    found_submission = False

    ticker_mentions = 0
    total_comments = 0

    # Fetch recent submissions from the subreddit
    for submission in reddit.subreddit(subreddit).new(limit=100):  # Adjust limit as needed
        submission_date = datetime.utcfromtimestamp(submission.created_utc)
        # Check if the submission is a Daily Discussion thread by flair and within the last 5 days
        if submission.link_flair_text == "Daily Discussion" and (today - submission_date).days <= 5:
            found_submission = True
            print(f"Found Daily Discussion Thread: {submission.title}")
             ## submission.comments.replace_more(limit=5)  # Load all comments
             # Directly iterate over top-level comments without expanding 'more comments'
            for comment in submission.comments:
                if isinstance(comment, praw.models.MoreComments):
                    continue  # Skip loading more comments
                total_comments += 1
                if ticker.lower() in comment.body.lower():
                    ticker_mentions += 1
            break  # Exit the loop once a submission is found

    # Calculate the percentage of comments that mention the ticker
    if total_comments > 0:
        percentage = (ticker_mentions / total_comments) * 100
    else:
        percentage = 0

    return percentage, ticker_mentions, total_comments, found_submission

# Example usage
ticker = "AAPL"  # Replace with the actual ticker
percentage, ticker_mentions, total_comments, found_submission = find_daily_discussion_comments(ticker)
if found_submission:
    print(f"Percentage of comments mentioning {ticker}: {percentage:.2f}%")
    print(f"Total comments: {total_comments}, Ticker mentions: {ticker_mentions}")
else:
    print("No Daily Discussion Thread found within the last 5 days.")
