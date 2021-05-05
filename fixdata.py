import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


def scale_array(scalar, arr):
    return [ele * scalar for ele in arr]


def scale_matrix(scalar, data):
    newData = []
    for list in data:
        newList = [v * scalar if v != 0 else v for v in list]
        newData.append(newList)
    return newData


'''
Gives a scatter plot of HRV against TL. 
'''


def plot_dot(HRV, TL):
    plt.plot(HRV, TL, 'bo', label='HRV against TL')
    plt.legend(loc="upper right")
    plt.ylabel('Träningsbelastning')
    plt.xlabel('HRV')
    plt.show()


'''
Plots the HRV data with the TL data. 
'''


def plot_hrv_tl(HRV, TL):
    plt.plot(TL, label='Training load')
    plt.plot(HRV, label='HRV')
    plt.legend(loc="upper right")
    plt.ylabel('Träningsbelastning')
    plt.xlabel('Dag')
    plt.show()


'''
Returns the HRV value that corresponds with workout by
comparing the date and name. 
'''


def check_hrv(dateWorkout, dateHRV, nameWorkout, nameHRV, HRV):
    c = 0
    for date, name in zip(dateHRV, nameHRV):
        time = date.date()
        time += timedelta(days=1)
        if time == dateWorkout.date() and name == nameWorkout:
            return HRV[c]
        c += 1


'''
Fixes the workout dates so that the correspond to the correct training day,
because sometimes the subjects do not send in the questionnaire the same day
as they train. 
'''


def fixDate(dateWorkout, trainingDay):
    newDateWorkout = dateWorkout.copy()
    weekDays = ("Måndag", "Tisdag", "Onsdag", "Torsdag", "Fredag", "Lördag", "Söndag")
    for x in range(len(dateWorkout)):
        dateTemp = dateWorkout[x].date()
        if str(trainingDay[x]) != "nan":
            while weekDays[dateTemp.weekday()] != str(trainingDay[x]):
                dateTemp -= timedelta(days=1)
        newDateWorkout[x] = dateTemp
    return newDateWorkout


'''
Returns the training load value that corresponds with HRV by comparing
the date and name.
'''


def check_workout(dateW, nameW, dateH, nameH, intensity, duration):
    for d in range(len(nameW)):
        time = dateW[d]
        timeHRV = dateH
        timeHRV -= timedelta(days=1)
        name = nameW[d]
        if time == timeHRV:
            name = str(name).lower()
            nameH = str(nameH).lower()
            if name.strip() == nameH.strip():
                return intensity[d] * duration[d]


'''
Replaces "None" in the matrix with 0. 
'''


def replace_none(data):
    newData = []
    for list in data:
        newList = [0 if v is None else v for v in list]
        newData.append(newList)
    return newData


HRVdata = []
EinarHRV = []
ThomasHRV = []
JonnyHRV = []
ChristerHRV = []
JessicaHRV = []
FilipHRV = []

TLdata = []
EinarTL = []
ThomasTL = []
JonnyTL = []
ChristerTL = []
JessicaTL = []
FilipTL = []

hrv = pd.read_excel('hrv.xlsx')
workout = pd.read_excel("training.xlsx")

training_Day = workout['Träningsdagen']
dateHRV = hrv['Tidstämpel']
'''
Makes so that the date corresponds to the correct training day
'''
dateWorkout = fixDate(workout['Tidstämpel'], training_Day)

intensity = workout['Hur intensiv kände du att träningen var?']
duration = workout['Hur länge varade träningspasset (i min):']

nameWorkout = workout['Namn:']
nameHRV = hrv['Namn:']

HRV = hrv['HRV']

'''
Fixes the array duration which can have strings that include minutes, min and so on.
It converts all to an integer of minutes. 
'''
durationCopy = np.zeros(len(duration))
k = 0
for d in duration:
    if 'minuter' in str(d):
        durationCopy[k] = int(str(d.replace('minuter', '')))
    elif 'min' in str(d):
        durationCopy[k] = int(str(d.replace('min', '')))
    elif ':' in str(d):
        x = d.index(':')
        durationCopy[k] = int(d[0:x]) * 60 + int(d[x + 1:])
    else:
        durationCopy[k] = d
    k += 1

duration = np.nan_to_num(durationCopy)  # Replaces all nan with 0

''' Sort out the workout data and append it to 
their respective array. The element that gets added to the TL arrays is the 
training load which is duration*intensity meanwhile HRV gets added to the HRV arrays.
check_workout checks so that the corresponding date matches. 
'''

for x in range(len(nameHRV)):
    namehrv = nameHRV[x].lower()
    if namehrv.strip() == 'c':
        ChristerHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        ChristerTL.append(tl_value)
    elif namehrv.strip() == 'einar ingemarsson':
        EinarHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        EinarTL.append(tl_value)
    elif namehrv.strip() == 'thomas':
        ThomasHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        ThomasTL.append(tl_value)
    elif namehrv.strip() == 'jessica':
        JessicaHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        JessicaTL.append(tl_value)
    elif namehrv.strip() == 'filip helmroth':
        FilipHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        FilipTL.append(tl_value)
    elif namehrv.strip() == 'jonny':
        JonnyHRV.append(HRV[x])
        tl_value = check_workout(dateWorkout, nameWorkout, dateHRV[x], nameHRV[x], intensity, duration)
        JonnyTL.append(tl_value)




'''
Put all the data into a matrix
'''
HRVdata.append(EinarHRV[1:])
HRVdata.append(ThomasHRV[2:])
HRVdata.append(JonnyHRV)
HRVdata.append(ChristerHRV)
HRVdata.append(JessicaHRV[1:])
HRVdata.append(FilipHRV[1:])
# print(HRVdata)

# print(JonnyHRV)
# print(JonnyTL)

TLdata.append(EinarTL[1:])
TLdata.append(ThomasTL[2:])
TLdata.append(JonnyTL)
TLdata.append(ChristerTL)
TLdata.append(JessicaTL[1:])
TLdata.append(FilipTL[1:])
# print(TLdata)

