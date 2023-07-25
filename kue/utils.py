import os
from keras.models import load_model
from keras.preprocessing.image import img_to_array, smart_resize
import numpy as np
from tensorflow import reshape



class Model():
    def __init__(self, model_path=os.path.join(os.getcwd(), 'kue', 'model', 'model.h5')):
        self.model_path = model_path
        self.class_names = [
            'kue_dadar_gulung',
            'kue_kastengel',
            'kue_klepon',
            'kue_lapis',
            'kue_lumpur',
            'kue_putri_salju',
            'kue_risoles',
            'kue_serabi'
        ]

    def predict(self, image):
        model = load_model(self.model_path)
        img = img_to_array(image)
        img = smart_resize(img, (224, 224))
        img = reshape(img, (-1, 224, 224, 3))
        prediction = model.predict(img/255)
        prediction = np.argmax(prediction)
        prediction = self.class_names[prediction]
        return prediction
    