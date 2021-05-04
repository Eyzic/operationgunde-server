import pandas as pd
import numpy as np
import datetime

def make_dataset_for_RNN(person,days_sequence ,start_day,end_day,hrv_dataframe,training_dataframe):
  # Load HRV Och Träningsdata
  hrv = hrv_dataframe
  training = training_dataframe
  # Make class for frames
  class frame_class:
    def __init__(self,date, name, sleep, stress,muscle_pain, humor , injuries,energi_level,training_load,RMSSD,SDNN,HRV_value):
      self.date = date
      self.name = name
      self.sleep = sleep
      self.stress = stress
      self.muscle_pain = muscle_pain
      self.humor = humor
      self.injuries = injuries
      self.energi_level = energi_level
      self.training_load = training_load
      self.RMSSD = RMSSD
      self.SDNN = SDNN
      self.HRV = HRV_value
  frame_list_hrv = []
  for i in range (hrv.shape[0]):
    day_ = int(hrv['Tidstämpel'][i].split()[0].split('-')[2])
    month_ = int(hrv['Tidstämpel'][i].split()[0].split('-')[1])
    date_ = datetime.date(int(hrv['Tidstämpel'][i].split()[0].split('-')[0]),month_,day_)
    name_ = hrv['Namn:'][i]
    sleep_ = hrv['Hur många timmar sov du i natt? '][i]
    stress_ = hrv['Stressnivå '][i]
    pain_ = hrv['Muskelvärk & muskeltrötthet'][i]
    humor_ = hrv['Humör '][i]
    injuries_ = hrv['Har du några skador? Ange graden på skadorna'][i]
    energy_ = float('NaN')
    RMSSD_ = hrv['RMSSD'][i]
    SDNN_ = hrv['SDNN'][i]
    HRV_value_ = hrv['HRV'][i]
    training_load_ = float('NaN')
    fr_ = frame_class(date_,name_,sleep_,stress_,pain_,humor_,injuries_,energy_,training_load_,RMSSD_,SDNN_,HRV_value_)
    frame_list_hrv.append(fr_)
  frame_list_training = []
  for i in range (training.shape[0]):
    date_ = datetime.date(int(training['Tidstämpel'][i].split()[0].split('-')[0]),int(training['Tidstämpel'][i].split()[0].split('-')[1]),int(training['Tidstämpel'][i].split()[0].split('-')[2]))
    date_ = date_ +datetime.timedelta(days = 1)
    name_ = training['Namn:'][i]
    sleep_ = float('NaN')
    stress_ = float('NaN')
    pain_ = float('NaN')
    humor_ =float('NaN')
    injuries_ = float('NaN')
    energy_ = training['Hur är din energinivå just nu?'][i]
    RMSSD_ = float('NaN')
    SDNN_ = float('NaN')
    HRV_value_ = float('NaN')
    if training['Hur länge varade träningspasset (i min):'][i]!=training['Hur länge varade träningspasset (i min):'][i]:
      continue
    if training['Hur länge varade träningspasset (i min):'][i]==0:
      training_load_ = 0
    if training['Hur länge varade träningspasset (i min):'][i]!=0:
      training_load_ = training['Hur intensiv kände du att träningen var?'][i]*training['Hur länge varade träningspasset (i min):'][i]
    fr_ = frame_class(date_,name_,sleep_,stress_,pain_,humor_,injuries_,energy_,training_load_,RMSSD_,SDNN_,HRV_value_)
    frame_list_training.append(fr_)



  for f in frame_list_training:
    name_ = f.name
    if name_ != name_:
      frame_list_training.remove(f)
      continue
    if len(name_)<2:
      name_='ch'
    else:
      name_ = name_[0:2].lower()
    f.name = name_
  for f in frame_list_hrv:
    name_ = f.name
    if len(name_)<2:
      name_='ch'
    else:
      name_ = name_[0:2].lower()
    f.name = name_




  for i in range(len(frame_list_hrv)):
    f = frame_list_hrv[i]
    days_ =0
    for j in range(len(frame_list_hrv)):
      f_compare= frame_list_hrv[j]
      if f.name == f_compare.name:
        if f.date == f_compare.date:
          days_ += 1
    frame_list_hrv[i] .date -= datetime.timedelta(days = days_-1)
  for i in range(len(frame_list_training)):
    f = frame_list_training[i]
    days_ =0
    for j in range(len(frame_list_training)):
      f_compare= frame_list_training[j]
      if f.name == f_compare.name:
        if f.date == f_compare.date:
          days_ += 1
    frame_list_training[i] .date -= datetime.timedelta(days=days_-1)

  # Delete the frame if training_load is nan
  for f in frame_list_training:
    if f.training_load != f.training_load:
      frame_list_training.remove(f)
  for f_hrv in frame_list_hrv:
    for f_tra in frame_list_training :
      if f_hrv.date != f_tra.date:
        continue
      if f_hrv.name != f_tra.name:
        continue
      f_hrv.energi_level = f_tra.energi_level
      f_hrv.training_load = f_tra.training_load


  frame_list = frame_list_hrv
  for f in frame_list:
    if f.training_load != f.training_load:
      frame_list.remove(f)

  col = ['date','name','sleep','muscle pain','humor','injuries','energy','training load','RMSSD','SDNN','HRV']
  d = pd.DataFrame()
  l_date = []
  l_name = []
  l_sleep = []
  l_stress = []
  l_muscle_pain = []
  l_humor = []
  l_injuries = []
  l_energy_level = []
  l_training_load = []
  l_RMSSD = []
  l_SDNN = []
  l_HRV = []
  for f in frame_list:
    l_date.append(f.date)
    l_name.append(f.name)
    l_sleep.append(f.sleep)
    l_stress.append(f.stress)
    l_muscle_pain.append(f.muscle_pain)
    l_humor.append(f.humor)
    l_injuries.append(f.injuries)
    l_energy_level.append(f.energi_level)
    l_training_load.append(f.training_load)
    l_RMSSD.append(f.RMSSD)
    l_SDNN.append(f.SDNN)
    l_HRV.append(f.HRV)


  d['date']=np.array(l_date)
  d['name']=np.array(l_name)
  d['sleep']=np.array(l_sleep)
  d['stress']=np.array(l_stress)
  d['muscle pain']=np.array(l_muscle_pain)
  d['humor']=np.array(l_humor)
  d['HRV']=np.array(l_HRV)
  d['injuries']=np.array(l_injuries)
  d['energy level']=np.array(l_energy_level)
  d['training load']=np.array(l_training_load)
  d['RMSSD']=np.array(l_RMSSD)
  d['SDNN']=np.array(l_SDNN)


  # Handling missing values
  # Handling missing values
  d['HRV'] = d['HRV'].fillna(d['HRV'].mean())
  d['muscle pain'] =d['muscle pain'].fillna(d['muscle pain'].mean())
  d['humor'] = d['humor'].fillna(d['humor'].mean())
  d['injuries'] = d['injuries'].fillna(d['injuries'].mean())
  d['energy level'] = d['energy level'].fillna(d['energy level'].mean())
  d_orig= d.dropna()

  # Sclaing data
  d = d_orig
  X_columns = d.drop(columns=['HRV','date','name','RMSSD','SDNN']).columns
  Y_columns = ['HRV']
  d_X = d[X_columns]
  d_Y = d[Y_columns]
  scaler_Y = MinMaxScaler(feature_range=(0,1)).fit(d[Y_columns].values.reshape(-1,1))

  scaler_X = MinMaxScaler(feature_range=(0,1)).fit(d[X_columns].values)

  d___ = d[Y_columns]
  d[Y_columns] = scaler_Y.transform(d___.values.reshape(-1,1))
  d___ = d[X_columns]
  d[ X_columns]= scaler_X.transform(d___.values)
  Columns = d.columns
  d.index = range(d.shape[0])
  # Making individual dataframes


  d_ind= pd.DataFrame(columns=Columns)
  name__ = person.name[0:2].lower  # Detta ska returnera 2 första bokstäver personens namn (små bokstäver)
  for x in range(d.shape[0]):

      if d['name'][x] == name__:
          d_ind = d_ind.append(pd.DataFrame(d.iloc[[x]], columns=Columns), ignore_index=True)



  # Make dataset compatible for RNN

  percentage_of_training_examples = 0.8
  list_dataframes = [d_ind]

  X_train = []
  Y_train = []

  for i in range(len(list_dataframes)):
    data_frame_ = list_dataframes[i].drop(columns = ['RMSSD','SDNN','date','name'])
    Y_data_frame = np.asarray(list_dataframes[i]['HRV']).astype ('float64')
    X_data_frame_ = np.asarray(data_frame_.values).astype('float64')
    for j in range (start_day,end_day):
      X_train.append(X_data_frame_[j-days_sequence:j])
      Y_train.append(Y_data_frame[j])

  X_train = np.array(X_train)
  Y_train = np.array(Y_train)
  return X_train,Y_train