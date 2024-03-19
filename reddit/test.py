from psaw import PushshiftAPI

api = PushshiftAPI()

results = list(api.search_submissions(q='question', subreddit='askreddit', filter=['title'], limit=10))

for result in results:
    print(result.title)