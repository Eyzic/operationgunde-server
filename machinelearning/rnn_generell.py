

def train_ind_model(model,X_train,Y_train):
    model.fit(X_train,Y_traing,epochs = 100,batch_size=1)
    return model
def predict_hrv_by_ind_model ( person,X):
    return person.rnnmodel.predict(X)