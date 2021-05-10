import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM,Dense,Dropout
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def optimize_training_by_RNN (person):
    X = []
    last_day = []
    optimized_TL=[]
    for i in range(6):
        X.append(Data_preprocessing.make_datasets_for_RNN(person,6,last_day, last_day,hrv_dataframe,training_dataframe)[i])#before updating HRV last day
    # Last row is the updated |for exampel that day the person updated his/her values like [10,2,6,9,NaN] where NaN is training load
    # put different training load in the frame and append X X.append(frame)
    # predict next days HRV for every alternative X data set
    return optimized_TL





