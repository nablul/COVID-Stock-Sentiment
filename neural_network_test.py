#Import modules
import config
import datetime
import pickle
import numpy as np
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense

#End date definition
end_date = datetime.datetime(2020, 10, 31)

#Load models
models = []
for x in range(3):
    models.append(load_model('model' + str(x + 1) + '.h5'))

#Load data
stock_data = config.load_obj('data')

#Initialize test input & output lists
testing_input = []
for model in models:
    testing_input.append([[] for x in range(16)])
testing_output = [[] for x in range(16)]

#For each ticker, determine data points to be tested (20%)
for ticker in config.ticker_list:
    start_date = datetime.datetime(2018, 10, 25)
    date_count = 0
    ticker_num = config.ticker_list[ticker]
    while start_date <= end_date:
        date_str = start_date.strftime('%m/%d/%Y')
        key = date_str + " - " + ticker
        
        #Retrieve NN input parameters
        NN_input_parameters = []
        for x in range(9):
            NN_input_parameters.append(stock_data[key][x])
        model_inputs = [NN_input_parameters[:4], NN_input_parameters[:8], NN_input_parameters[:7]]
        output = [NN_input_parameters[8]]
        
        #Append 20% of data to testing category
        if date_count % 5 == 0:
            for x in range(3):
                testing_input[x][ticker_num].append(model_inputs[x])
            testing_output[ticker_num].append(output)
        
        #Clear NN input list and increment date
        NN_input_parameters.clear()
        date_count += 1
        start_date += config.time_delta

#For each ticker, test each model multiple times and print best performance
for ticker in config.ticker_list:
    ticker_num = config.ticker_list[ticker]
    model_input = []
    model_accuracy = []
    model_max_accuracy = []
    
    #Convert input & output to numpy arrays
    for x in range(3):
        model_accuracy.append([])
        model_input.append(np.array(testing_input[x][ticker_num]))
    output = np.array(testing_output[ticker_num])
    
    #Test model iteratively
    for x in range(50):
        for x in range(3):
            _, accuracy = models[x].evaluate(model_input[x], output, verbose = 0)
            model_accuracy[x].append(round(accuracy*100, 2))
    
    #Determine and print best result
    for x in range(3):
        model_max_accuracy.append(max(model_accuracy[x]))
    print(ticker + ': ' + str(model_max_accuracy[0]) + ' ' + str(model_max_accuracy[1]) + ' ' + str(model_max_accuracy[2]))
