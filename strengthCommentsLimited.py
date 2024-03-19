from datetime import datetime, timedelta
import praw

# Initialize PRAW with your Reddit app credentials
reddit = praw.Reddit(client_id='QyyiKi73QvFJqi_nX9ALQg',
                     client_secret='njKqQqY8r2JEn_V4SuWrg1uNn2FJig',
                     user_agent='fetchWSB')

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
            submission.comments.replace_more(limit=20)  # Attempt to load up to 1000 comments
            comment_list = submission.comments.list()
            # If the list is too large, slice it to the first 1000 comments
            comment_list = comment_list[:2000]
            for comment in comment_list:
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
ticker = "apple"  # Replace with the actual ticker
percentage, ticker_mentions, total_comments, found_submission = find_daily_discussion_comments(ticker)
if found_submission:
    print(f"Percentage of comments mentioning {ticker}: {percentage:.2f}%")
    print(f"Total comments: {total_comments}, Ticker mentions: {ticker_mentions}")
else:
    print("No Daily Discussion Thread found within the last 5 days.")
