#Import modules
import datetime
import pickle

#New York Times API Key
nyt_API_key = "WcZlETd7MyNORGGPCcnGe1eUs4mLxEKG"

#List of stocks/tickers
ticker_list = {'BAC': 0, 'JPM': 1, 'BRK.A': 2, 'GS': 3, 'AAPL': 4, 'CSCO': 5, 'INTC': 6, 'ORCL': 7, 'TSLA': 8, 'AMZN': 9, 'EBAY': 10, 'MCD': 11, 'FB': 12, 'GOOG': 13, 'CMCSA': 14, 'VZ': 15}

#Tickers and full names of corresponding companies
ticker_fullname = {'BAC': "Bank of America", 'JPM': "JP Morgan", 'BRK.A': "Berkshire", 'GS': "Goldman Sachs", 'AAPL': "Apple", 'CSCO': "Cisco", 'INTC': "Intel", 'ORCL': "Oracle", 'TSLA': "Tesla", 'AMZN': "Amazon", 'EBAY': "Ebay", 'MCD': "McDonald's", 'FB': "Facebook", 'GOOG': "Google", 'CMCSA': "Comcast", 'VZ': "Verizon"}

#Market sectors and corresponding stocks/tickers
market_ticker = {"FIN" : ['BAC', 'JPM', 'BRK.A', 'GS'], "INF" : ['AAPL', 'CSCO', 'INTC', 'ORCL'], "CON" : ['TSLA', 'AMZN', 'EBAY', 'MCD'], "COM" : ['FB', 'GOOG', 'CMCSA', 'VZ']}

#Stocks/Tickers and corresponding market sectors
ticker_market = {'BAC': "FIN", 'JPM': "FIN", 'BRK.A': "FIN", 'GS': "FIN", 'AAPL': "INF", 'CSCO': "INF", 'INTC': "INF", 'ORCL': "INF", 'TSLA': "CON", 'AMZN': "CON", 'EBAY': "CON", 'MCD': "CON", 'FB': "COM", 'GOOG': "COM", 'CMCSA': "COM", 'VZ': "COM"}

#Date unit definiton
time_delta = datetime.timedelta(days = 1)

#Function to save dict as .pickle
def save_obj(obj, name):
    f = open(name + '.pickle', "wb")
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#Function to save dict from .pickle
def load_obj(name):
    f = open(name + '.pickle', "rb")
    return pickle.load(f)
