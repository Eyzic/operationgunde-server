import pandas as pd

import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import LSTM,Dense,Dropout
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from keras.models import load_model

import math

def train_general_model(model,X_train,Y_train):
    model.fit(X_train,Y_train,epochs = 100,batch_size=1)
    return model
def predict_hrv_by_general_RNN_model (general_model,X):
    return general_model.predict(X)