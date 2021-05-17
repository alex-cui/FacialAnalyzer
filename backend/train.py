import cv2 as cv
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
import os
import numpy as np
from mtcnn.mtcnn import MTCNN
import PIL

import keras
from keras.models import Sequential, model_from_json
import keras.layers as layers
from keras.preprocessing.image import ImageDataGenerator
from keras.optimizers import Adam

import shutil
import test

def guess_age_of_faces():
    batch_size = 32
    img_size = 180

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        'cropped_photos/',
        validation_split = .2,
        subset = 'training',
        seed = 123,
        image_size = (img_size, img_size),
        batch_size = batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        'cropped_photos/',
        validation_split = .2,
        subset = 'validation',
        seed = 123,
        image_size = (img_size, img_size),
        batch_size = batch_size
    )
    class_names = train_ds.class_names
    print(class_names)
    print(train_ds)
    print(val_ds)

    # plt.figure(figsize = (10, 10))
    # for images, labels in train_ds.take(1):
    #     for i in range(9):
    #         ax = plt.subplot(3, 3, i + 1)
    #         plt.imshow(images[i].numpy().astype('uint8'))
    #         plt.title(class_names[labels[i]])
    #         plt.axis('off')
    # plt.show()
    # for image_batch, labels_batch in train_ds:
    #     print(image_batch.shape)
    #     print(labels_batch.shape)

    # data_augmentation = keras.Sequential([
    #     layers.experimental.preprocessing.RandomFlip('horizontal', input_shape = (img_size, img_size, 3)),
    #     layers.experimental.preprocessing.RandomRotation(.1),
    #     layers.experimental.preprocessing.RandomZoom(.1)
    # ])

    json_path = 'age.json'
    num_classes = 5

    if os.path.isfile(json_path):
        json_file = open(json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights('age.h5')
        print('Loaded model from disk')
        loaded_model.compile(optimizer = 'adam',
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
        metrics = ['accuracy'])

        for image in os.listdir('test'):
            img = keras.preprocessing.image.load_img(
                'test/' + image, target_size = (img_size, img_size)
            )

            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            predictions = loaded_model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                '{} most likely belongs to {} with a {:.2f} percent confidence.'
                .format(image, class_names[np.argmax(score)], 100 * np.max(score))
            )

    else:
        model = Sequential([
            # data_augmentation,
            layers.experimental.preprocessing.Rescaling(1./255, input_shape = (img_size, img_size, 3)),
            layers.Conv2D(16, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Dropout(.2),
            layers.Flatten(),
            layers.Dense(128, activation = 'relu'),
            layers.Dense(num_classes)
        ])
        model.compile(optimizer = 'adam',
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
        metrics = ['accuracy'])
        model.summary()

        epochs = 10
        history = model.fit(
            train_ds,
            validation_data = val_ds,
            epochs = epochs
        )
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs_range = range(epochs)

        plt.figure(figsize = (8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label = 'Training Accuracy')
        plt.plot(epochs_range, val_acc, label = 'Validation Accuracy')
        plt.legend(loc = 'lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label = 'Training Loss')
        plt.plot(epochs_range, val_loss, label = 'Validation Loss')
        plt.legend(loc = 'upper right')
        plt.title('Training and Validation Loss')

        plt.show()

        model_json = model.to_json()
        with open('age.json', 'w') as json_file:
            json_file.write(model_json)
        model.save_weights('age.h5')
        print('Saved Model to Disk')

        for image in os.listdir('test'):
            img = keras.preprocessing.image.load_img(
                'test/' + image, target_size = (img_size, img_size)
            )

            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                '{} most likely belongs to {} with a {:.2f} percent confidence.'
                .format(image, class_names[np.argmax(score)], 100 * np.max(score))
            )

def guess_gender_of_faces():
    batch_size = 32
    img_size = 180

    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        'cropped_gender/',
        validation_split = .2,
        subset = 'training',
        seed = 123,
        image_size = (img_size, img_size),
        batch_size = batch_size
    )
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        'cropped_gender/',
        validation_split = .2,
        subset = 'validation',
        seed = 123,
        image_size = (img_size, img_size),
        batch_size = batch_size
    )
    class_names = train_ds.class_names
    print(class_names)
    print(train_ds)
    print(val_ds)

    # plt.figure(figsize = (10, 10))
    # for images, labels in train_ds.take(1):
    #     for i in range(9):
    #         ax = plt.subplot(3, 3, i + 1)
    #         plt.imshow(images[i].numpy().astype('uint8'))
    #         plt.title(class_names[labels[i]])
    #         plt.axis('off')
    # plt.show()
    # for image_batch, labels_batch in train_ds:
    #     print(image_batch.shape)
    #     print(labels_batch.shape)

    data_augmentation = keras.Sequential([
        layers.experimental.preprocessing.RandomFlip('horizontal', input_shape = (img_size, img_size, 3)),
        layers.experimental.preprocessing.RandomRotation(.1),
        layers.experimental.preprocessing.RandomZoom(.1)
    ])

    json_path = 'gender.json'
    num_classes = 2

    if os.path.isfile(json_path):
        json_file = open(json_path, 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights('gender.h5')
        print('Loaded model from disk')
        loaded_model.compile(optimizer = 'adam',
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
        metrics = ['accuracy'])

        for image in os.listdir('test'):
            img = keras.preprocessing.image.load_img(
                'test/' + image, target_size = (img_size, img_size)
            )

            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            predictions = loaded_model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                '{} most likely belongs to {} with a {:.2f} percent confidence.'
                .format(image, class_names[np.argmax(score)], 100 * np.max(score))
            )
    else:
        model = Sequential([
            data_augmentation,
            layers.experimental.preprocessing.Rescaling(1./255, input_shape = (img_size, img_size, 3)),
            layers.Conv2D(16, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(32, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, 3, padding = 'same', activation = 'relu'),
            layers.MaxPooling2D(),
            layers.Dropout(.2),
            layers.Flatten(),
            layers.Dense(128, activation = 'relu'),
            layers.Dense(num_classes)
        ])
        model.compile(optimizer = 'adam',
        loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
        metrics = ['accuracy'])
        model.summary()

        epochs = 15
        history = model.fit(
            train_ds,
            validation_data = val_ds,
            epochs = epochs
        )
        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs_range = range(epochs)

        plt.figure(figsize = (8, 8))
        plt.subplot(1, 2, 1)
        plt.plot(epochs_range, acc, label = 'Training Accuracy')
        plt.plot(epochs_range, val_acc, label = 'Validation Accuracy')
        plt.legend(loc = 'lower right')
        plt.title('Training and Validation Accuracy')

        plt.subplot(1, 2, 2)
        plt.plot(epochs_range, loss, label = 'Training Loss')
        plt.plot(epochs_range, val_loss, label = 'Validation Loss')
        plt.legend(loc = 'upper right')
        plt.title('Training and Validation Loss')

        plt.show()

        model_json = model.to_json()
        with open('gender.json', 'w') as json_file:
            json_file.write(model_json)
        model.save_weights('gender.h5')
        print('Saved Model to Disk')

        for image in os.listdir('test'):
            img = keras.preprocessing.image.load_img(
                'test/' + image, target_size = (img_size, img_size)
            )

            img_array = keras.preprocessing.image.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)
            predictions = model.predict(img_array)
            score = tf.nn.softmax(predictions[0])

            print(
                '{} most likely belongs to {} with a {:.2f} percent confidence.'
                .format(image, class_names[np.argmax(score)], 100 * np.max(score))
            )

def draw_faces(filename, directory, name, result_list):
    data = plt.imread(filename)
    new_filename = ''
    for i in range (len(result_list)):
        x1, y1, width, height = result_list[i]['box']
        x2, y2 = x1 + width, y1 + height
        plt.subplot(1, len(result_list), i + 1)
        plt.axis('off')
        if data[y1:y2, x1:x2].shape[0] <= 0 or data[y1:y2, x1:x2].shape[1] <= 0:
            continue
        plt.imshow(data[y1:y2, x1:x2])
        new_filename = 'cropped_gender/' + directory[7:] + '/' + name[0:-4] + '_' + str(i) + '.png'
        plt.savefig(new_filename, bbox_inches='tight')
        plt.clf()
        plt.cla()

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
        if os.stat(photo[1]).st_size <= 1048576:
            print(photo[1])
            pixels = cv.imread(photo[1])
            # print(pixels)
            # pixels = tf.convert_to_tensor(pixels[:,:,:3])
            # print(pixels.shape)

            faces = detector.detect_faces(pixels)
            # print(faces)
            cropped_url = draw_faces(photo[1], path, photo[0], faces)
            print(cropped_url)
            shutil.move(photo[1], 'gender/done_male/' + photo[0])



def guess(json_path, b64):
    json_file = open(json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(json_path[0:-5] + '.h5')
    print('Loaded model from disk')
    loaded_model.compile(optimizer = 'adam',
    loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits = True),
    metrics = ['accuracy'])

    class_names = []

    if json_path == 'age.json':
        class_names = ['baby', 'child', 'middle_aged', 'senior', 'youth']
    else:
        class_names = ['male', 'female']

    img_size = 180

    img = test.readb64(b64)
    img2 = cv.resize(img, (img_size, img_size))
    img = img2[:,:, ::-1]

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)
    predictions = loaded_model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    return {
        "class" : class_names[np.argmax(score)],
        "confidence" : round(100 * np.max(score), 2)
    }
    # print(
    #     '{} most likely belongs to {} with a {:.2f} percent confidence.'
    #     .format('Photo', class_names[np.argmax(score)], 100 * np.max(score))
    # )


def main():

    # define_age_of_faces()
    # crop_photos('gender/male')
    # guess('age.json', b64)
    # guess('gender.json', b64)
    # guess_gender_of_faces()
    # print('hello')

    return


if __name__ == '__main__':
    main()
