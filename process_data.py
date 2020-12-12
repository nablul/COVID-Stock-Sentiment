#Import modules
import config
import datetime
import pickle
import sentiment_analysis

#End date definition
end_date = datetime.datetime(2020, 10, 31)

#Function to normalize data within 0 and 1, based on max and min of range
def normalize(data, max, min, rounding):
    data_norm = data + abs(min)
    max_norm = max + abs(min)
    min_norm = min + abs(min)
    normalized_data = (data_norm - min_norm)/(max_norm - min_norm)
    return round(normalized_data, rounding)

#Load data
stock_data = config.load_obj('stock-data')
stock_news = config.load_obj('stock-news')
top_news = config.load_obj('top-news')

#Determine stock news sentiment
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        stock_news[key] = sentiment_analysis.news_sentiment(stock_news[key])
        start_date += config.time_delta

#Determine COVID-19 news sentiment from top news headlines
start_date = datetime.datetime(2018, 10, 25)
while start_date <= end_date:
    date_str = start_date.strftime('%m/%d/%Y')
    key = date_str
    top_news[key] = sentiment_analysis.COVID_sentiment(top_news[key])
    start_date += config.time_delta

#3-day average of stock news sentiments
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 27)
    while start_date <= end_date:
        day_1 = start_date - (2*config.time_delta)
        day_2 = start_date - (config.time_delta)
        day_3 = start_date
        day_1_key = day_1.strftime('%m/%d/%Y') + " - " + ticker
        day_2_key = day_2.strftime('%m/%d/%Y') + " - " + ticker
        day_3_key = day_3.strftime('%m/%d/%Y') + " - " + ticker
        stock_news[day_3_key] = (stock_news[day_1_key] + stock_news[day_2_key] + stock_news[day_3_key])/3
        start_date += config.time_delta

#3-day average of COVID-19 news sentiments
start_date = datetime.datetime(2018, 10, 27)
while start_date <= end_date:
    day_1 = start_date - (2*config.time_delta)
    day_2 = start_date - (config.time_delta)
    day_3 = start_date
    day_1_key = day_1.strftime('%m/%d/%Y')
    day_2_key = day_2.strftime('%m/%d/%Y')
    day_3_key = day_3.strftime('%m/%d/%Y')
    top_news[day_3_key] = (top_news[day_1_key] + top_news[day_2_key] + top_news[day_3_key])/3
    start_date += config.time_delta

#Normalize stock news between 0 and 1
#Determine max & min of news sentiment scores
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 25)
    max_sentiment = -100000000000000000
    min_sentiment = 100000000000000000
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        if stock_news[key] > max_sentiment:
            max_sentiment = stock_news[key]
        if stock_news[key] < min_sentiment:
            min_sentiment = stock_news[key]
        start_date += config.time_delta
    
    #Determine max & min of news sentiment scores
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        stock_news[key] = normalize(stock_news[key], max_sentiment, min_sentiment, 4)
        start_date += config.time_delta

#Normalize COVID-19 news between 0 and 1
#Determine max & min of news sentiment scores
start_date = datetime.datetime(2018, 10, 25)
max_sentiment = -100000000000000000
min_sentiment = 100000000000000000
while start_date <= end_date:
    date_str = start_date.strftime('%m/%d/%Y')
    key = date_str
    if top_news[key] > max_sentiment:
        max_sentiment = top_news[key]
    if top_news[key] < min_sentiment:
        min_sentiment = top_news[key]
    start_date += config.time_delta

# Normalize data based on max & min values of sentiment scores
start_date = datetime.datetime(2018, 10, 25)
while start_date <= end_date:
    date_str = start_date.strftime('%m/%d/%Y')
    key = date_str
    top_news[key] = normalize(top_news[key], max_sentiment, min_sentiment, 4)
    start_date += config.time_delta

#Normalize stock data between 0 and 1
# For each ticker, determine max & min values of parameters
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 25)
    max_values = [-100000000000000000] * 4
    min_values = [100000000000000000] * 4
    
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        for index in range(4):
            if float(stock_data[key][index]) > max_values[index]:
                max_values[index] = float(stock_data[key][index])
            if float(stock_data[key][index]) < min_values[index]:
                min_values[index] = float(stock_data[key][index])
        start_date += config.time_delta
    
    # Normalize data based on max & min values of parameters
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        for index in range(4):
            stock_data[key][index] = normalize(float(stock_data[key][index]), max_values[index], min_values[index], 4)
        start_date += config.time_delta
    
    max_values.clear()
    min_values.clear()

#Determine market sector news sentiment
market_sentiment = {}
for market in config.market_ticker:
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        sentiment = 0
        date_str = start_date.strftime('%m/%d/%Y')
        for ticker in config.market_ticker[market]:
            key = date_str + " - " + ticker
            sentiment += stock_news[key]
        sentiment = round(sentiment/len(config.market_ticker[market]), 4)
        market_sentiment_tag = date_str + " - " + market
        market_sentiment[market_sentiment_tag] = sentiment
        start_date += config.time_delta

#Determine average of all sectors news sentiments
all_sentiment = {}
start_date = datetime.datetime(2018, 10, 25)
while start_date <= end_date:
    sentiment = 0
    date_str = start_date.strftime('%m/%d/%Y')
    for ticker in config.ticker_list:
        key = date_str + " - " + ticker
        sentiment += stock_news[key]
    sentiment = round(sentiment/len(config.ticker_list), 4)
    all_sentiment_tag = date_str
    all_sentiment[all_sentiment_tag] = sentiment
    start_date += config.time_delta

#Collect all data into single dict
for ticker in config.ticker_list:
    market = config.ticker_market[ticker]
    
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        date_key = date_str
        date_ticker_key = date_str + " - " + ticker
        date_market_key = date_str + " - " + market
        stock_data[date_ticker_key].append(stock_news[date_ticker_key])
        stock_data[date_ticker_key].append(market_sentiment[date_market_key])
        stock_data[date_ticker_key].append(all_sentiment[date_key])
        stock_data[date_ticker_key].append(top_news[date_key])
        start_date += config.time_delta

#Determine output value for NN
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 25)
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        next_date = start_date + config.time_delta
        next_date_str = next_date.strftime('%m/%d/%Y')
        next_date_key = next_date_str + " - " + ticker
        if start_date == end_date:
            stock_data[key].append(1)
        else:
            next_date_price = stock_data[next_date_key][0]
            current_date_price = stock_data[key][0]
            if next_date_price > current_date_price:
                stock_data[key].append(1)
            else:
                stock_data[key].append(0)
        start_date += config.time_delta
        
#Save data
config.save_obj(stock_data, 'data')
