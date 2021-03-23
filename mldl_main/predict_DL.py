from django.conf import settings
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import array_to_img, img_to_array, load_img
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image # pillow
import cv2 # opencv-python
import pickle


def predict_cnn_one(path):

    base_url = settings.MEDIA_ROOT_URL + settings.MEDIA_URL
    model_url = base_url + 'Ingredien_classifier(Xception).h5'
    model = models.load_model(model_url, compile=False)
    name_code = pickle.load(open( base_url + 'name_code.pickle', 'rb'))

    new_img = load_img(path, target_size=(299,299))
    arr_img = img_to_array(new_img)
    img = arr_img.reshape((1,) + arr_img.shape)
    img = img.astype('float32')/255

    num_code = model.predict_proba(img).argmax()
    proba = model.predict(img).max() * 100

    for key, value in name_code.items():
        if num_code == value: name = key

    name = name.replace('_', ' ')

    return name
