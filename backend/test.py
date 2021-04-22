import cv2 as cv
import mtcnn

image_number = 0

def image_text():
    global image_number
    text = 'images/'
    num = str(image_number)
    for i in range(5 - len(num)):
        text += '0'
    text += num
    text += '.png'
    image_number += 1
    return text


classifier = cv.CascadeClassifier('haarcascade_frontalface_default.xml')

for i in range(10):
    pixels = cv.imread(image_text())

    bboxes = classifier.detectMultiScale(pixels)

    for box in bboxes:
        x, y, width, height = box
        x2, y2 = x + width, y + height
        cv.rectangle(pixels, (x, y), (x2, y2), (0, 0, 255), 1)

    cv.imshow('face detection', pixels)
    cv.waitKey(0)
    cv.destroyAllWindows()






