
from tensorflow import keras


def train_general_model(model_path,X_train,Y_train):
    model = keras.models.load_model(model_path)
    model.fit(X_train,Y_train,epochs = 100,batch_size=1)
    return model
def predict_hrv_by_general_RNN_model (general_model_path,X):
    model = keras.models.load_model(general_model_path)
    return model.predict(X)

