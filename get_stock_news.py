#Import modules
import config
import datetime
import pickle
from pynytimes import NYTAPI

#Define nyt access instance per API key
nyt = NYTAPI(config.nyt_API_key)

#For each stock/ticker for each day, download news and append to list of news
for ticker in config.ticker_fullname:
    articles_dict = {}
    start_date = datetime.datetime(2018, 10, 25)
    end_date = datetime.datetime(2020, 10, 31)
    
    #For each day download news and append to list of news
    while start_date <= end_date:
        articles_list = []
        articles = nyt.article_search(
            query = config.ticker_fullname[ticker],
            results = 10,
            dates = {"begin": start_date, "end": start_date + config.time_delta}
        )
        for article in articles:
            articles_list.append(article['abstract'])
        articles_dict[start_date.strftime('%m/%d/%Y')] = articles_list
        #Print current ticker & date
        print(ticker + " - " + start_date.strftime('%m/%d/%Y'))
        start_date += config.time_delta

    #Save data
    config.save_obj(articles_dict, ticker)
