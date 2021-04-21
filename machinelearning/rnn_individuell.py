import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM,Dense,Dropout

from sklearn.preprocessing import MinMaxScaler, StandardScaler
class individual_rnn:
    def __init__(self,ind_rnn_model,input_dataset,output_dataset):
        self.ind_rnn_model = ind_rnn_model
        self.input_dataset = input_dataset
        self.output_dataset = output_dataset