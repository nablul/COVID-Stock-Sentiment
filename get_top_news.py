#Import modules
import config
import datetime
import pickle
from pynytimes import NYTAPI

#Define nyt access instance per API key
nyt = NYTAPI(config.nyt_API_key)

#Initialize dict to store news
news_dict = {}
start_date = datetime.datetime(2018, 10, 25)
end_date = datetime.datetime(2020, 10, 31)

#For each day, download news and append to list of news
while start_date <= end_date:
    news_list = []
    articles = nyt.article_search(
        query = "",
        results = 20,
        dates = {"begin": start_date, "end": start_date + config.time_delta}
    )
    for article in articles:
        news_list.append(article['abstract'])
    news_dict[start_date.strftime('%m/%d/%Y')] = news_list
    print(start_date.strftime('%m/%d/%Y'))
    start_date += config.time_delta

#Save data
config.save_obj(news_dict, "top-news")
