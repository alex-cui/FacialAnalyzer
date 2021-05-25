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
import io
from imageio import imread
from PIL import Image
import time


def draw_faces(filename, directory, name, result_list):
    data = pyplot.imread(filename)
    new_filename = ''
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


def crop_photos(path):
    photos = []
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
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
    new_filename = ''
    pictures = []

    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        if data[y1:y2, x1:x2].shape[0] <= 0 or data[y1:y2, x1:x2].shape[1] <= 0:
            continue
        pyplot.imshow(data[y1:y2, x1:x2])
        buf = io.BytesIO()
        pyplot.savefig(buf, format = 'png')
        buf.seek(0)
        bytes = np.asarray(bytearray(buf.read()), dtype = np.uint8)
        buf.close()
        im = cv.imdecode(bytes, cv.IMREAD_COLOR)
        pictures.append(im)

        #
        # #file name is time + 1
        # new_filename = 'cropped_photos/' + directory + '/' + name + str(i) + '.png'
        # pyplot.savefig(new_filename, bbox_inches='tight')
        # pyplot.clf()
        # pyplot.cla()
        # fileNames.append('/' + name + str(i) + '.png')

    return pictures


def detect(image):
    print("IN TEST.PY")#finally has img url
    print(image)

    detector = MTCNN()
    pixels = readb64(image)

    faces = detector.detect_faces(pixels)
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)


    pictures = drawFaces(image, "main", current_time, faces)
    b64Images = []

    for picture in pictures:
        print(picture)
        retval, buffer = cv.imencode('.png', picture)
        b64_val = base64.b64encode(buffer)
        b64Images.append(b64_val)

    return b64Images #return how many faces were found


def readb64(uri):
   encoded_data = uri.split(',')[1]
   # encoded_data = uri
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv.imdecode(nparr, cv.IMREAD_COLOR)
   img2 = img[:,:, ::-1]
   return img2



def main():
    # change to data/(baby, child, youth, middle_aged, or senior)
    # make sure you have a directory like cropped_photos/baby and cropped_photos/child ... etc
    # if you want you can add a new folder into data to receive the images
    # but make sure you add a new folder into cropped_folders with the same name
    # crop_photos('data/child')
    # crop_photos('data/new')
    # image = cv.imread('12234.jpg')
    # retval, buffer = cv.imencode('.png', image)
    # b64 = base64.b64encode(buffer)
    # b64 = 's,' + str(b64)
    # l = detect(b64)
    return

if __name__ == '__main__':
    main()
