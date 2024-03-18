from datetime import datetime, timedelta
import praw

# Initialize PRAW with your Reddit app credentials
reddit = praw.Reddit(client_id='QyyiKi73QvFJqi_nX9ALQg',
                     client_secret='njKqQqY8r2JEn_V4SuWrg1uNn2FJig',
                     user_agent='fetchWSB')

def find_daily_discussion_comments(ticker, subreddit="wallstreetbets"):
    """Find the percentage of comments mentioning the ticker in the nearest past Daily Discussion thread within 7 attempts."""
    today = datetime.now()
    attempts = 0
    max_attempts = 7
    found_submission = False

    ticker_mentions = 0
    total_comments = 0

    while not found_submission and attempts < max_attempts:
        # Adjust the target day based on the number of attempts
        target_day = today - timedelta(days=1 + attempts)
        target_day_str = target_day.strftime('%Y-%m-%d')

        # Use flair_name:"Daily Discussion" in the search query
        search_query = f'flair_name:"Daily Discussion" timestamp:{int(target_day.timestamp())}..{int((target_day + timedelta(days=1)).timestamp())}'

        for submission in reddit.subreddit(subreddit).search(search_query, sort='new', syntax='cloudsearch', limit=1):
            found_submission = True
            submission.comments.replace_more(limit=None)  # Load all comments
            for comment in submission.comments.list():
                total_comments += 1
                if ticker.lower() in comment.body.lower():
                    ticker_mentions += 1
            break  # Exit the loop once a submission is found

        attempts += 1

    # Calculate the percentage of comments that mention the ticker
    if total_comments > 0:
        percentage = (ticker_mentions / total_comments) * 100
    else:
        percentage = 0

    return percentage, ticker_mentions, total_comments, attempts

# Example usage
ticker = "apple"  # Replace with the actual ticker
percentage, ticker_mentions, total_comments, attempts = find_daily_discussion_comments(ticker)
if attempts < 7:
    print(f"Found after {attempts} attempts.")
    print(f"Percentage of comments mentioning {ticker}: {percentage:.2f}%")
    print(f"Total comments: {total_comments}, Ticker mentions: {ticker_mentions}")
else:
    print("No Daily Discussion Thread found within the past 7 days.")
