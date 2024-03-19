# test files to interact with reddit and alphavantage APIs for use in a stock analysis tool

## sentiment indicators

### reddit scripts

#### strengthSubmissions.py
    finds percent of posts mentioning specificed ticker in last 48 hours relative to mentions in past 30
        so its how 'popular' a particular ticker in the past 48 hours based on its 30 day popularity

#### strengthCommentsLimited.py 
    finds proxy percent of comments in daily thread that mention specified tickers
        stopped functioning - wsb subreddit removed filter flair

#### strengthCommentsTitleFilter.py
    finds proxy percent of comments in daily thread that mention specified tickers
        but looks for "Daily Discussion Thread" in submission title instead
        loads up to 20 more comments underneath each top level comment // replace.more(limit:n)

#### strengthTLCommentsTitleFilter.py
    finds proxy percent of comments in daily thread that mention specified tickers
        but looks for "Daily Discussion Thread" in submission title instead
        iterates over only the top level comments


## technical indicators

### financial modeling scripts

#### stockList.py
    returns json filtering for non-penny stocks (price > 5$) in the NYSE & NASDAQ
        endpoint used: https://financialmodelingprep.com/api/v3/stock/list
        ** live data at time of call
        info in json: symbol, price, name, exchange, type


#### stockScreener.py
    returns json filtering based on predefined parameter criteria
        endpoint used: https://financialmodelingprep.com/api/v3/stock-screener
        ** limited to 1000 results per call, so only 1000 per exchange
            criteria would need to be more specific

#### exchangeSymbol
    returns json of all symbols under exchanges based on custom criteria
        endpoint used: https://financialmodelingprep.com/api/v3/symbol/
        ** have to do extra step to refine list before outputting to json
