import os
import cv2
from keras.models import model_from_json
import numpy as np
from scipy import ndimage
import sklearn
from django.conf import settings
from sklearn.externals import joblib
import keras.backend.tensorflow_backend
import tensorflow as tf
import numpy as np
from imageio import imread, imsave
from .preprocess.normalize import remove_background, remove_background1
from . import signet_spp_300dpi
from .cnn_model import CNNModel
from .models import * 

def Account_Number_Extraction(st):

    form=cv2.imread(st,0)
    crop=cv2.resize(form, (1992,1000),interpolation=cv2.INTER_CUBIC)
    [x, y, w, h] = [440, 40 , 550, 57]
    acc = crop[y:y+h,x:x+w]

    # return the list of sorted contours and bounding boxes
    def sort_contours(cnts):
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),key=lambda b:b[1][0]))
        return (cnts, boundingBoxes)

    model_path = os.path.join(settings.MEDIA_ROOT,'MNIST_Weights/model_MNIST.json')
    json_file = open(model_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(os.path.join(settings.MEDIA_ROOT,'MNIST_Weights/model_MNIST.h5'))
    # evaluate loaded model on test data
    loaded_model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    #account number
    acc_num=""
    ret, mask = cv2.threshold(acc, 180, 255, cv2.THRESH_BINARY_INV)
    mask=cv2.erode(mask,(3,3),iterations=2)
    _, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts,bx=sort_contours(contours)

    for contour in cnts:
        [x, y, w, h] = cv2.boundingRect(contour)
        if w>20 and w<40 and h>30 and h<60:
            new_img=mask[y:y+h,x:x+w]
            new_img=cv2.resize(new_img, (18,18),interpolation=cv2.INTER_CUBIC)
            padded_digit = np.pad(new_img, ((5,5),(5,5)), "constant", constant_values=0)
            ans=loaded_model.predict(padded_digit.reshape(1,28,28,1)).tolist()[0]
            acc_num=acc_num+str((ans.index(max(ans))))
            
    return acc_num

def Signature_Extraction(st,sp):
    form=cv2.imread(st,0)
    crop=cv2.resize(form, (1992,1000),interpolation=cv2.INTER_CUBIC)
    [x,y,w,h] = [600,720,720,130]
    sign = crop[y:y+h,x:x+w]
    user1_sigs  = [imread(sp.Image_Path.path),sign]
    processed_user1_sigs_spp = [255-remove_background(user1_sigs[0]),255-remove_background1(user1_sigs[1]) ]
    model = CNNModel(signet_spp_300dpi, os.path.join(settings.MEDIA_ROOT,'models/signet_spp_300dpi.pkl'))
    user1_features_spp = [model.get_feature_vector(sig, layer='fc2') for sig in processed_user1_sigs_spp]
    dist = np.linalg.norm(user1_features_spp[0] - user1_features_spp[1])
    return dist