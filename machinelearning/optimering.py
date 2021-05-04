import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM,Dense,Dropout
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler


# Load model general and individual
ind_model = keras.models.load_model('filepath')
general_model =  keras.models.load_model('filepath')


# load the data set and make  data sets compatible to the RNN

# Make a list of all possible data sets for intensity  1-10
list_datasets = []
current_predicted_HRV = 0
optimized_intensity=0
for dataset in list:
    #Predict HRV
    predicted_HRV = ind_model.predict(dataset)
    if predicted_HRV > current_predicted_HRV:
        current_predicted_HRV =predicted_HRV
        optimized_intensity = [] # Intensity used for the dataset




