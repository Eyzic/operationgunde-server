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

# Load  individual models
model = load_model('path')
dataset = [] # Current data set compatible
X = []
Y = []
# train models
model.fit(X,Y,batch_size=1,epochs=20)

# Save trained models
keras.models.save_model('path') #



