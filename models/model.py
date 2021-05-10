import math
import random
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn import preprocessing
from sklearn.metrics import r2_score

from models.thomas_preprocessing import newHRV, newTL, TLdata, HRVdata, scale_array, newRMSSD

def removezeros(tlarr, hrvarr):
    for x in range(len(tlarr)):
        if tlarr[x] == 0:
            hrvarr[x] = 0
    return tlarr, hrvarr


def g(tl, CTLC):
    g_arr = []
    for x in range(len(tl)):
        if not g_arr and tl[x] != 0:
            g_arr.append(tl[x])
        elif g_arr:
            i = 1
            k = len(g_arr) - 1
            while g_arr[k] == 0:
                i += 1
                k -= 1
            t = g_arr[k]
            g_arr.append(t * np.exp(-i / CTLC) + tl[x])
    return g_arr


def g_(tl, CTLC, g_temp):
    g_arr = []
    for x in range(len(tl)):

        if not g_arr:
            g_arr.append(g_temp[-1] * np.exp(-1 / CTLC) + tl[x])
        elif not g_arr and tl[x] == 0:
            g_arr.append(g_temp[-1])
        elif g_arr:
            i = 1
            k = len(g_arr) - 1
            while g_arr[k] == 0:
                i += 1
                k -= 1
            t = g_arr[k]
            g_arr.append(t * np.exp(-i / CTLC) + tl[x])
    return g_arr


def h(tl, ATLC):
    h_arr = []
    for x in range(len(tl)):
        if not h_arr and tl[x] != 0:
            h_arr.append(tl[x])
        elif h_arr:
            i = 1
            k = len(h_arr) - 1
            while h_arr[k] == 0:
                i += 1
                k -= 1
            t = h_arr[k]
            h_arr.append(t * np.exp(-i / ATLC) + tl[x])
    return h_arr


def h_(tl, ATLC, h_temp):
    h_arr = []
    for x in range(len(tl)):
        if not h_arr and tl[x] != 0:
            h_arr.append(h_temp[-1] * np.exp(-1 / ATLC) + tl[x])
        elif not h_arr and tl[x] == 0:
            h_arr.append(h_temp[-1])
        elif h_arr:
            i = 1
            k = len(h_arr) - 1
            while h_arr[k] == 0:
                i += 1
                k -= 1
            t = h_arr[k]
            h_arr.append(t * np.exp(-i / ATLC) + tl[x])
    return h_arr


# Banister model
def Banister(params):
    losses = []
    performance = []
    k1, k2, P0, CTLC, ATLC = params

    g_data = g(tl_train, CTLC)
    h_data = h(tl_train, ATLC)

    for i in range(len(g_data)):
        fitness = g_data[i]
        fatigue = h_data[i]
        performance.append(k1 * fitness - k2 * fatigue + P0)

    performance = np.array(performance)
    performance = performance.reshape(-1, 1)
    performance = scaler2.transform(performance)

    # print("after scaling ", performance)
    # performance = preprocessing.normalize([performance])
    # performance = performance.ravel()

    for i in range(len(g_data)):
        loss = abs(hrv_train[i] - performance[i]) ** 2
        losses.append(loss)
    ResidualSum = np.mean(losses) / len(losses)
    return ResidualSum


def Banistermodel(k1, k2, P0, CTLC, ATLC):
    performance = []
    g_data = g(tl_train, CTLC)
    h_data = h(tl_train, ATLC)

    # print("g_data for train", g_data)
    # print("h_data for train", h_data)
    for i in range(len(g_data)):
        fitness = g_data[i]
        fatigue = h_data[i]
        performance.append(k1 * fitness - k2 * fatigue + P0)

    performance = np.array(performance)
    performance = performance.reshape(-1, 1)
    performance = scaler2.transform(performance)

    # performance = preprocessing.normalize([performance])
    # performance = performance.ravel()
    # print("test: ", performance)
    return np.array(performance), g_data, h_data


def Banistermodel_predict(k1, k2, P0, CTLC, ATLC):
    performance = []
    p, testg, testh = Banistermodel(k1, k2, P0, CTLC, ATLC)
    g_data = g_(tl_test, CTLC, testg)
    h_data = h_(tl_test, ATLC, testh)

    # print("len of tl_test:",len(tl_test))
    # print("g_data for test", g_data)
    # print("h_data for test", h_data)
    for i in range(len(g_data)):
        fitness = g_data[i]
        fatigue = h_data[i]
        performance.append(k1 * fitness - k2 * fatigue + P0)

    performance = np.array(performance)
    performance = performance.reshape(-1, 1)
    performance = scaler2.transform(performance)
    return np.array(performance)


scaler = MinMaxScaler()
scaler2 = MinMaxScaler()

'''
Normalize data
'''
# newTL[1] = preprocessing.normalize([newTL[1]])
# newTL[1] = newTL[1].ravel()

# print(newTL[1])
'''
Split up data to train and test data
'''

allTL = newTL[0] + newTL[1] + newTL[2] + newTL[3] + newTL[4]
allHRV = newHRV[0] + newHRV[1] + newHRV[2] + newHRV[3] + newHRV[4]
tl_train = np.array(allTL[0:150])
hrv_train = np.array(allHRV[0:150])

tl_test = np.array(allTL[151:])
hrv_test = np.array(allHRV[151:])
# tl_train = np.array(newTL[5][0:30])
# hrv_train = np.array(newHRV[5][0:30])
#
# tl_test = np.array(newTL[5][31:40])
# hrv_test = np.array(newHRV[5][31:40])

print(newHRV[5])
# tl_train = np.array(newTL[1][0:30])
# hrv_train = np.array(newRMSSD[0][0:30])
#
# tl_test = np.array(newTL[1][31:])
# hrv_test = np.array(newRMSSD[0][31:])
df = pd.DataFrame({'hrv': hrv_train})

# print(df)
df = df.ewm(span=7).mean()

# print(df)
hrv_train = np.transpose(df.to_numpy()).ravel()
hrv_neural = hrv_train
# print(np.transpose(df.to_numpy()).ravel())
testscale = hrv_train.reshape(-1, 1)
scaler2.fit(testscale)

# print("tl_train: ", tl_train)
# print("hrv_train: ", hrv_train)
#
# print("tl_test: ", tl_test)
# print("hrv_test: ", hrv_test)

# print(len(newTL[5]))

# Data for neural

tl_neural = tl_train

'''
Banister model
'''
# intial_values = np.array([0.5, 0.5, 50, 10, 10])
intial_values = np.array([0.0000767, 0.0000893, 0, 20, 11])
test = minimize(Banister, intial_values, options={'disp': False})
per, notg, noth = Banistermodel(test.x[0], test.x[1], test.x[2], test.x[3], test.x[4])
# print(per)
banister_hrv = Banistermodel_predict(test.x[0], test.x[1], test.x[2], test.x[3], test.x[4])
# print("g_data for tl", g(newTL[3], test.x[3]))
# print("h_data for tl", h(newTL[3], test.x[4]))
# print(test.x[2])
'''
Scale data for neural network
'''

tl_neural = tl_neural.reshape(-1, 1)
tl_test = tl_test.reshape(-1, 1)
tl_train = tl_train.reshape(-1, 1)

# print("tl_neural before: ", tl_neural)
scaler.fit(tl_neural)
tl_neural = scaler.transform(tl_neural)
tl_test = scaler.transform(tl_test)

print("tl_neural: ", tl_neural)
print("hrv_neural: ", hrv_neural)
# print("tl_neural after: ", tl_neural)


neural_model = MLPRegressor(solver='lbfgs', activation="relu", hidden_layer_sizes=[50], random_state=42, max_iter=500)
neural_model.fit(tl_neural, hrv_neural)
predicted_hrv = neural_model.predict(tl_test)
trained_hrv = neural_model.predict(tl_neural)

# print("banister_hrv:", len(banister_hrv))
# print("hrv_test:", len(hrv_test))
# '''
# Print out the Mean Squared error for the different models
# '''
print("Neural MSE = ", mean_squared_error(predicted_hrv, hrv_test))
print("Neural RMSE = ", mean_squared_error(predicted_hrv, hrv_test, squared=False))
print("Banister MSE = ", mean_squared_error(banister_hrv, hrv_test))
print("Banister RMSE = ", mean_squared_error(banister_hrv, hrv_test, squared=False))
print("Neural r2-score on tuning data =", r2_score(hrv_train, trained_hrv))
print("Banister r2-score on tuning data =", r2_score(hrv_train, per))
print("Neural r2-score on test data =", r2_score(hrv_test, predicted_hrv))
print("Banister r2-score on test data =", r2_score(hrv_test, banister_hrv))
# print("Neural Predicted hrv: ", predicted_hrv)
# print("True hrv: ", hrv_test)
# print("Banister predicted hrv: ", banister_hrv)
# # rint("test_y: ", predicted_hrv)
# # print("hrv_test:", hrv_test)
X = trained_hrv.tolist() + predicted_hrv.tolist()

'''
Plot the data
'''
# plt.plot(hrv_train, 'o', label='HRV')

plt.plot(per.tolist() + banister_hrv.tolist(), label='BanisterpredictedHRV')
# plt.legend(loc="upper right")
# plt.show()
plt.plot(hrv_train.tolist() + hrv_test.tolist(), 'o', label='HRV')
plt.plot(X, label='NeuralpredictedHRV')
plt.legend(loc="upper right")
plt.ylabel('HRV')
plt.xlabel('Dag')
# plt.ylim([3, 4.2])
plt.show()
scaler3 = MinMaxScaler()
testscale = hrv_train.reshape(-1, 1)
scaler3.fit(testscale)

# print("g before:", notg)

# test1 = np.array(notg)
# test1 = test1.reshape(-1, 1)
#
# # print("h before:", noth)
# test2 = np.array(noth)
# test2 = test2.reshape(-1, 1)
#
# test1 = scaler3.transform(test1)
# test2 = scaler3.transform(test2)

# print("g:", test1)
# print("h:",test2)

# plt.plot(test1, label = 'Fitness')
# plt.plot(test2, label = "Fatigue")
# plt.show()
