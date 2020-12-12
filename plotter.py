#Import modules
import config
import datetime
import pickle
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

#Load data
stock_data = config.load_obj('data')

#Function to plot stock parameters for a list of attributes
def plotter(title, ticker, attribute, start_date = "10/25/2018", end_date = "10/31/2020"):
    #Map between attribute and index in stock_data dict
    attribute_map = {'price' : 0, 'volume' : 1, 'low' : 2, 'high' : 3, 'stock_sent' : 4, 'sector_sent' : 5, 'market_sent' : 6, 'covid_sent' : 7}
    #End date definition
    end_date_time_obj = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    #Axis formatting for dates
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%y-%b')
    months_fmt = mdates.DateFormatter('%b')
    
    #Plot parameters
    plt.figure(figsize = (10, 7.5))
    plt.title(title, fontsize = 25)
    plt.xlabel('Year-Month', fontsize = 16)
    plt.ylabel('Normalized Range', fontsize = 16)
    ax = plt.gca()
    formatter = mdates.DateFormatter("%Y-%m-%d")
    ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)
    
    #For each attribute, retrieve data from stock_data and plot graph
    for a in attribute:
        start_date_time_obj = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        dates = []
        values = []
        row = attribute_map[a]
        while start_date_time_obj <= end_date_time_obj:
            key = start_date_time_obj.strftime('%m/%d/%Y') + " - " + ticker
            dates.append(start_date_time_obj)
            values.append(stock_data[key][row])
            start_date_time_obj += config.time_delta
        plt.plot(dates, values, label = a, linewidth = 1)

    #Adjust plot graphics and print/save graph
    plt.setp(ax.get_xticklabels(), rotation = 75)
    plt.legend(loc = 2, prop={'size': 16})
    plt.savefig(title + '.png', bbox_inches='tight')
    plt.show()

#Function call
plotter('AAPL Price & COVID-19 Sentiment', 'AAPL', ['price', 'covid_sent'], "10/31/2018", "10/31/2020")
