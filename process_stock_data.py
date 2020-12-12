#Import modules
import config
import datetime
import pickle
import csv
import statistics

#Load data
stock_data ={}

#for each ticker, open stock data .csv and append data to stock_data
for ticker in config.ticker_list:
    filename = ticker + "-Table 1.csv"

    #Open file
    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        
        #Read and append data to stock_data
        row_count = 0
        for row in readCSV:
            if row_count == 0:
                row_count += 1
            else:
                date_str = row[1]
                date_time_obj = datetime.datetime.strptime(date_str, '%m/%d/%Y %H:%M:%S')
                key = date_time_obj.strftime('%m/%d/%Y') + " - " + ticker
                stock_data[key] = [row[2], row[4], row[6], row[8]]
                row_count += 1
   
    #Start and End time definition
    start_date = datetime.datetime(2018, 10, 25)
    end_date = datetime.datetime(2020, 10, 31)
    
    #Scan data for days with missing information. If found: missing info = avg of prev & next day
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        
        #Determine previous and next day containing data
        if key not in stock_data:
            prev_key = key
            next_key = key
            prev_date = start_date
            next_date = start_date
            while prev_key not in stock_data:
                prev_key = (prev_date - config.time_delta).strftime('%m/%d/%Y') + " - " + ticker
                prev_date -= config.time_delta
            while next_key not in stock_data:
                next_key = (next_date + config.time_delta).strftime('%m/%d/%Y') + " - " + ticker
                next_date += config.time_delta
            
            #Determine average and append to stock_data
            price = statistics.mean([float(stock_data[prev_key][0]), float(stock_data[next_key][0])])
            volume = statistics.mean([float(stock_data[prev_key][1]), float(stock_data[next_key][1])])
            low = statistics.mean([float(stock_data[prev_key][2]), float(stock_data[next_key][2])])
            high = statistics.mean([float(stock_data[prev_key][3]), float(stock_data[next_key][3])])
            stock_data[key] = [price, volume, low, high]
        start_date += config.time_delta

#Save data
config.save_obj(stock_data, "stock-data")
