# test files to interact with reddit and alphavantage APIs for use in a stock analysis tool

## scripts

### strengthSubmissions.py
    finds percent of posts mentioning specificed ticker in last 48 hours relative to mentions in past 30
        so its how 'popular' a particular ticker in the past 48 hours based on its 30 day popularity

### strengthCommentsLimited.py 
    finds proxy percent of comments in daily thread that mention specified tickers
        stopped functioning - wsb subreddit removed filter flair

### strengthCommentsTitleFilter.py
    finds proxy percent of comments in daily thread that mention specified tickers
        but looks for "Daily Discussion Thread" in submission title instead
        loads up to 20 more comments underneath each top level comment // replace.more(limit:n)

### strengthTLCommentsTitleFilter.py
    finds proxy percent of comments in daily thread that mention specified tickers
        but looks for "Daily Discussion Thread" in submission title instead
        iterates over only the top level comments



