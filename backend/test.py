import cv2 as cv
import seaborn as sns
from matplotlib import pyplot
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
import os
import numpy as np
from mtcnn.mtcnn import MTCNN

import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

# import urllib
from skimage import io
import matplotlib
import base64
import io as asdf
from imageio import imread
from PIL import Image


# def image_text():
#    global image_number
#    text = 'data/images/'
#    num = str(image_number)
#    for i in range(5 - len(num)):
#        text += '0'
#    text += num
#    text += '.png'
#    image_number += 1
#    return text

# classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
#
# time_spent = 0
# cv.setUseOptimized(False)
# pixels = cv.imread('data/baby/11601.jpg')
# interval = cv.getTickCount()
# bboxes = classifier.detectMultiScale(pixels)
#
# for box in bboxes:
#     x, y, width, height = box
#     x2, y2 = x + width, y + height
#     cv.rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)
#
# cv.imshow('Face detection', pixels)
# time_spent += (cv.getTickCount() - interval)/cv.getTickFrequency()
# print('Total Time:', time_spent)
# cv.waitKey(0)
# cv.destroyAllWindows()

def draw_faces(filename, directory, name, result_list):
    data = pyplot.imread(filename)
    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        pyplot.imshow(data[y1:y2, x1:x2])
        new_filename = 'cropped_photos/' + directory[5:] + '/' + name[0:-4] + '_' + str(i) + '.png'
        pyplot.savefig(new_filename, bbox_inches='tight')
        pyplot.clf()
        pyplot.cla()

    # pyplot.show()
    return new_filename

def get_data(data_dir):
    data = []
    image_size = 300
    for label in labels:
        path = os.path.join(data_dir, label)
        class_num = labels.index(label)
        for img in os.listdir(path):
            try:
                img_arr = cv.imread(os.path.join(path, img))[...,::,-1]
                resized_arr = cv.resize(img_arr, (image_size, image_size))
                data.append([resized_arr, class_num])
            except Exception as e:
                print(e)
    return np.array(data)


def define_age_of_faces():
    labels = ['baby', 'child', 'youth', 'middle_aged', 'senior']

    train = get_data('data/')
    validation = get_data('data/')
    l = []


    image_number = 0

def crop_photos(path):
    photos = []
    with os.scandir(path) as it:
        for entry in it:
            if (entry.name.endswith('.png') or entry.name.endswith('.jpg')) and entry.is_file():
                photos.append((entry.name, entry.path))
    detector = MTCNN()
    for photo in photos:
        print(photo[1])
        pixels = pyplot.imread(photo[1])
        print(pixels)

        faces = detector.detect_faces(pixels)
        # print(faces)
        print(draw_faces(photo[1], path, photo[0], faces))


def drawFaces(filename, directory, name, result_list):
    matplotlib.use('agg')
    data = readb64(filename)
    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        pyplot.imshow(data[y1:y2, x1:x2])
        new_filename = 'cropped_photos/' + directory + '/' + name + str(i) + '.png'
        pyplot.savefig(new_filename, bbox_inches='tight')
        pyplot.clf()
        pyplot.cla()


def detect(image):
    print("IN TEST.PY")#finally has img url
    print(image[0:100])

    detector = MTCNN()
    pixels = readb64(image)

    faces = detector.detect_faces(pixels)
    drawFaces(image, "main", "f", faces)
    return len(faces) #return how many faces were found


def readb64(uri):
   encoded_data = uri.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   return img



def main():
    # change to data/(baby, child, youth, middle_aged, or senior)
    # make sure you have a directory like cropped_photos/baby and cropped_photos/child ... etc
    # if you want you can add a new folder into data to receive the images
    # but make sure you add a new folder into cropped_folders with the same name
    crop_photos('data/child')

    # pixels = pyplot.imread(filename)
    # detector = MTCNN()
    # faces = detector.detect_faces(pixels)
    # print(faces)
    #
    # new_filename = draw_faces(filename, faces)
    # print(new_filename)
    # pixels2 = pyplot.imread(new_filename)
    # print(pixels2)
    # detector2 = MTCNN()
    return

if __name__ == '__main__':
    main()
