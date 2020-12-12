#Import modules
import config
import datetime
import pickle
import numpy as np
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense

#End date definition
end_date = datetime.datetime(2020, 10, 31)

#Load data
stock_data = config.load_obj('data')

#Neural network design parameters
epoch = 150
batch = 10
activation_function_1 = 'relu'
activation_function_2 = 'sigmoid'
loss_function = 'binary_crossentropy'
optimizer_function = 'Adam'
metrics_function = ['accuracy']
hidden_layer1_size = 10
hidden_layer2_size = 6
output_layer_size = 1
input_layer_size = [4, 8, 7]

#Initialize test input & output lists
training_input = [[], [], []]
training_output = []

#For each ticker, determine data points to be used for training (80%)
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
        
        #Append 80% of data to training category
        if date_count % 5 != 0:
            for x in range(3):
                training_input[x].append(model_inputs[x])
            training_output.append(output)
        
        #Clear NN input list and increment date
        NN_input_parameters.clear()
        date_count += 1
        start_date += config.time_delta

#Establish sequential NN models
model1 = Sequential()
model2 = Sequential()
model3 = Sequential()
models = [model1, model2, model3]

#Define, compile and evaluate each model
training_output = np.array(training_output)
for x in range(3):
    #Establish model architecture
    training_input[x] = np.array(training_input[x])
    models[x].add(Dense(hidden_layer1_size, input_dim = input_layer_size[x], activation = activation_function_1))
    models[x].add(Dense(hidden_layer2_size, activation = activation_function_1))
    models[x].add(Dense(output_layer_size, activation = activation_function_2))
    #Compile model
    models[x].compile(loss = loss_function, optimizer = optimizer_function, metrics = metrics_function)
    #Fit model
    models[x].fit(training_input[x], training_output, epochs = epoch, batch_size = batch)
    #Save model
    models[x].save('model' + str(x + 1) + '.h5')
