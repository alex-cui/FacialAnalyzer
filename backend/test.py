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

def draw_faces(filename, directory, name, result_list):
    data = pyplot.imread(filename)
    new_filename = ''
    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        if data[y1:y2, x1:x2].shape[0] <= 0 or data[y1:y2, x1:x2].shape[1] <= 0:
            continue
        # print(data[y1:y2, x1:x2].shape)
        pyplot.imshow(data[y1:y2, x1:x2])
        new_filename = 'cropped_photos/' + directory[5:] + '/' + name[0:-4] + '_' + str(i) + '.png'
        pyplot.savefig(new_filename, bbox_inches='tight')
        pyplot.clf()
        pyplot.cla()
    return new_filename

def crop_photos(path):
    photos = []
    with os.scandir(path) as it:
        for entry in it:
            if (entry.name.endswith('.png') or entry.name.endswith('.jpg')) and entry.is_file():
                photos.append((entry.name, entry.path))
    detector = MTCNN()
    for photo in photos:
        print(photo[0])
        pixels = pyplot.imread(photo[1])
        faces = detector.detect_faces(pixels)
        draw_faces(photo[1], path, photo[0], faces)
        # print(draw_faces(photo[1], path, photo[0], faces))

def get_data(data_dir, labels):
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

    train = get_data('cropped_photos/', labels)
    validation = get_data('cropped_photos/', labels)
    # print(train)
    # print(validation)


    image_number = 0


def main():
    # change to data/(baby, child, youth, middle_aged, or senior)
    # make sure you have a directory like cropped_photos/baby and cropped_photos/child ... etc
    # if you want you can add a new folder into data to receive the images
    # but make sure you add a new folder into cropped_folders with the same name
    # crop_photos('data/baby')
    # crop_photos('data/child')
    # crop_photos('data/youth')
    # crop_photos('data/middle_aged')
    crop_photos('data/senior')

    define_age_of_faces()

    return

if __name__ == '__main__':
    main()
