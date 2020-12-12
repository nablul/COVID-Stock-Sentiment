#Import modules
import config
import datetime
import pickle
import numpy as np
from numpy.random import rand
from numpy.random import seed
from scipy.stats import spearmanr

#Load data
stock_data = config.load_obj('data')

#Function to print Spearman's Correlation between (2) attributes for all tickers between start and end dates
def correlation_calculator(attribute_1, attribute_2, start_date = "10/25/2018", end_date = "10/31/2020"):
    #Map between attribute and index in stock_data dict
    attribute_map = {'price': 0, 'volume': 1, 'low': 2, 'high': 3, 'stock_sent': 4, 'sector_sent': 5, 'market_sent': 6, 'covid_sent': 7}
    #Batch of days to calculate Spearman's correlation
    day_increment = 10
    #Retrive corresponding attribute values
    index_1 = attribute_map[attribute_1]
    index_2 = attribute_map[attribute_2]
    
    #End date definition
    end_date_time_obj = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    
    ticker_correlation_coeffs = []
    
    #For each ticker, iterate through dates between start & end dates -> Calculate correlation
    for ticker in config.ticker_list:
        correlation_coeffs = []
        data_1 = []
        data_2 = []
        date_count = 0
        
        #Iterate through all dates in batch increments
        start_date_time_obj = datetime.datetime.strptime(start_date, '%m/%d/%Y')
        while start_date_time_obj <= end_date_time_obj:
            #Batch size reached -> calculate correlation coefficient and append to list (if not nan)
            if date_count % day_increment == 0 and date_count != 0:
                coeff, p = spearmanr(data_1, data_2)
                if np.isnan(coeff) == False:
                    correlation_coeffs.append(coeff)
                data_1.clear()
                data_2.clear()
            #Batch size not reached -> append data to list of data
            key = start_date_time_obj.strftime('%m/%d/%Y') + " - " + ticker
            data_1.append(stock_data[key][index_1])
            data_2.append(stock_data[key][index_2])
            date_count += 1
            start_date_time_obj += config.time_delta
       
        #Calculate correlation for remaining data in buffer and append to list (if not nan)
        coeff, p = spearmanr(data_1, data_2)
        if np.isnan(coeff) == False:
            correlation_coeffs.append(coeff)
        
        #Calculate average correlation coefficient for ticker and print result
        avg_correlation_coeff = round(sum(correlation_coeffs)/len(correlation_coeffs), 2)
        ticker_correlation_coeffs.append(avg_correlation_coeff)
        print(ticker + ': ' + str(avg_correlation_coeff))
    
    #Calculate and print average correlation coefficient across all tickers
    total_avg_correlation_coeff = round(sum(ticker_correlation_coeffs)/len(ticker_correlation_coeffs), 2)
    print('Average Correlation Coefficient for ' + attribute_1 + ' & ' + attribute_2 + ' is: ' + str(total_avg_correlation_coeff))

#Function call
correlation_calculator('price', 'covid_sent', '10/25/2018', '10/31/2020')
