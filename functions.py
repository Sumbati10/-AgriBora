import os
import pickle
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.models import load_model

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def get_model(path):
    model = load_model(path, compile=False)
    return model

def img_predict(path, crop):
    data = load_img(path, target_size=(224, 224, 3))
    data = np.asarray(data).reshape((-1, 224, 224, 3))
    data = data * 1.0 / 255
    model = get_model(os.path.join(BASE_DIR, 'models', 'DL_models', f'{crop}_model.h5'))
    if len(crop_diseases_classes[crop]) > 2:
        predicted = np.argmax(model.predict(data)[0])
    else:
        p = model.predict(data)[0]
        predicted = int(np.round(p)[0])
    return predicted

def get_diseases_classes(crop, prediction):
    crop_classes = crop_diseases_classes[crop]
    return crop_classes[prediction][1].replace("_", " ")

def get_crop_recommendation(item):
    scaler_path = os.path.join(BASE_DIR, 'models', 'ML_models', 'crop_scaler.pkl')
    model_path = os.path.join(BASE_DIR, 'models', 'ML_models', 'crop_model.pkl')

    with open(scaler_path, 'rb') as f: