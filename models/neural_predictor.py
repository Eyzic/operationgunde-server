from sklearn.neural_network import MLPRegressor
import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pandas as pd

from models.thomas_preprocessing import newHRV, newTL, TLdata, HRVdata, scale_array, newRMSSD, nameWorkout, data, intensity, duration

def dropna(HRV, TL):
    df = pd.concat([HRV, TL], axis=1)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df


def HRV_tomorrow(Name):
    x = len(nameWorkout)-1
    while nameWorkout[x] != Name:
        x -= 1
    TLtoPredict = intensity[x]*duration[x]
    TLHRV = dropna(data[Name+'HRV'], data[Name+'TL'])
    HRVarr = TLHRV[Name+'HRV'].to_numpy()
    TLarr = TLHRV[Name+'TL'].to_numpy()
    HRVpredicted = runmodel(HRVarr, TLarr, TLtoPredict)
    return HRVpredicted




def runmodel(HRVarr, TLarr, TLpredict):
    allTL = TLarr
    allHRV = HRVarr
    df = pd.DataFrame({'hrv': allHRV})
    df = df.ewm(span=7).mean()

    scaler = MinMaxScaler()
    allHRV = np.transpose(df.to_numpy()).ravel()
    TLpredict = np.array(TLpredict).reshape(-1,1)
    X = allTL.reshape(-1, 1)
    y = allHRV.reshape(-1, 1).ravel()
    scaler.fit(X)
    X = scaler.transform(X)
    regr = MLPRegressor(solver="lbfgs", activation="tanh", random_state=50, hidden_layer_sizes=[100], max_iter=2000).fit(X, y)
    X_test = scaler.transform(TLpredict)
    return regr.predict(X_test)

#allTL = np.array(newTL[1]) #+ newTL[1] + newTL[2] + newTL[3] + newTL[4])
#allHRV = np.array(newHRV[5]) #+ newHRV[1] + newHRV[2] + newHRV[3] + newHRV[4])
#allHRV = np.array(newRMSSD[0])
#allTL = allTL[0:40]

#print("Before: ", allTL)

# df = pd.DataFrame({'hrv': allHRV})
# df = df.ewm(span=7).mean()
# dl = pd.DataFrame({'TL': allTL})
# dl = dl.ewm(span=40).mean()

# print(df)
# print(df)
#allHRV = np.transpose(df.to_numpy()).ravel()
#allTL = np.transpose(dl.to_numpy()).ravel()
#print("After: ", allTL)

#X, y = make_regression(n_samples=200, random_state=42)
# X = allTL.reshape(-1, 1)
# y = allHRV.reshape(-1, 1).ravel()
# X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, shuffle= False, train_size= 0.75)
#
# scaler.fit(X_train)
# X_train = scaler.transform(X_train)
# regr = MLPRegressor(solver = "lbfgs",activation="tanh", random_state=50, hidden_layer_sizes=[100],max_iter=500).fit(X_train, y_train)
# X_test = scaler.transform(X_test)
# y_pred = regr.predict(X_test)
# print("MSE = ", mean_squared_error(y_pred, y_test))
# print(len(X_test))
# print(len(X_train))
# print(regr.score(X_test, y_test))
# tuned = regr.predict(X_train)
# print(r2_score(y_pred, y_test))
# plt.plot(tuned.tolist()+y_pred.tolist(), label='Neural model')
# #plt.plot(y_train, 'o', )
# plt.plot(allHRV, 'o', label = 'Real HRV')
#
#
# # plt.plot(X, label='NeuralpredictedHRV')
# # plt.legend(loc="upper right")
# # plt.ylabel('HRV')
# # plt.xlabel('Dag')
# plt.show()



