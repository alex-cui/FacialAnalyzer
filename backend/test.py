import cv2 as cv
import seaborn as sns
from matplotlib import pyplot
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
import os
import numpy as np
from mtcnn.mtcnn import MTCNN

labels = ['baby', 'child','youth', 'middle_aged', 'senior']
image_size = 300
def get_data(data_dir):
    data = []
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

# train = get_data('data/')
l = []


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

# classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

# time_spent = 0
# cv.setUseOptimized(False)
# for i in range(10):
#     pixels = cv.imread(image_text())
#     interval = cv.getTickCount()
#     bboxes = classifier.detectMultiScale(pixels)

#     for box in bboxes:
#         x, y, width, height = box
#         x2, y2 = x + width, y + height
#         cv.rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)

#     cv.imshow('Face detection', pixels)
#     time_spent += (cv.getTickCount() - interval)/cv.getTickFrequency()
#     print('Total Time:', time_spent)
#     cv.waitKey(0)
#     cv.destroyAllWindows()

def draw_faces(filename, result_list):
    data = pyplot.imread(filename)
    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        pyplot.subplot(1, len(result_list), i + 1)
        pyplot.axis('off')
        pyplot.imshow(data[y1:y2, x1:x2])
    pyplot.show()

def main():
    print(tf.__version__)
    filename = image_text()
    pixels = pyplot.imread(filename)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    draw_faces(filename, faces)
    return

if __name__ == '__main__':
    main()






