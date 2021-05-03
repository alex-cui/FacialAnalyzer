import cv2 as cv
import seaborn as sns
from matplotlib import pyplot
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
import os
import numpy as np

import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPool2D , Flatten , Dropout 
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

labels = ['baby', 'kid','teenager', 'adult', 'elderly']
image_size = 300
def get_data(data_dir):
    data = []
    for label in labels:
        path  = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv2.imread(os.path.join(path, img))[...,::,-1]
                resized_arr = cv2.resize(img_arr, (img_size, img_size))
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)

train = get_data('data/')
l = []
for i in train:




image_number = 0

def image_text():
    global image_number
    text = 'data/images/'
    num = str(image_number)
    for i in range(5 - len(num)):
        text += '0'
    text += num
    text += '.png'
    image_number += 1
    return text

classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

time_spent = 0
cv.setUseOptimized(False)
for i in range(10):
    pixels = cv.imread(image_text(), 0)
    interval = cv.getTickCount()
    bboxes = classifier.detectMultiScale(pixels)

    for box in bboxes:
        x, y, width, height = box
        x2, y2 = x + width, y + height
        cv.rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)

    cv.imshow('Face detection', pixels)
    time_spent += (cv.getTickCount() - interval)/cv.getTickFrequency()
    print('Total Time:', time_spent)
    cv.waitKey(0)
    cv.destroyAllWindows()








