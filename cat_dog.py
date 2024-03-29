# -*- coding: utf-8 -*-
"""cat_dog.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18-oFjN4Ylvz9f5MvJp20GzTwgwcZpU2H
"""

# Commented out IPython magic to ensure Python compatibility.
try:
  # This command only in Colab.
#   %tensorflow_version 2.x
except Exception:
  pass
import tensorflow as tf

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, Flatten, Dropout, BatchNormalization, MaxPooling2D,Input
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications import VGG16

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

import os
import numpy as np
import matplotlib.pyplot as plt

# Get project files
# !wget https://cdn.freecodecamp.org/project-data/cats-and-dogs/cats_and_dogs.zip

# !unzip cats_and_dogs.zip

PATH = '/content/cats_and_dogs'

train_dir = os.path.join(PATH, 'train')
validation_dir = os.path.join(PATH, 'validation')
test_dir = os.path.join(PATH, 'test')

# Get number of files in each directory. The train and validation directories
# each have the subdirecories "dogs" and "cats".
total_train = sum([len(files) for r, d, files in os.walk(train_dir)])
total_val = sum([len(files) for r, d, files in os.walk(validation_dir)])
total_test = len(os.listdir(test_dir))

# Variables for pre-processing and training.
batch_size = 128
epochs = 20
IMG_HEIGHT = 224
IMG_WIDTH = 224

# 3
train_image_generator = ImageDataGenerator(
    rescale=1./255
)
validation_image_generator= ImageDataGenerator(rescale=1./255,)
test_image_generator=ImageDataGenerator(rescale=1./255)

train_data_gen =train_image_generator.flow_from_directory(
    '/content/cats_and_dogs/train',
     target_size=(224, 224),
     batch_size=128,
     class_mode='binary',

)
val_data_gen = validation_image_generator.flow_from_directory(
     '/content/cats_and_dogs/validation',
     target_size=(224, 224),
     batch_size=128,
     class_mode='binary'

)
test_data_gen = test_image_generator.flow_from_directory(
    '/content/cats_and_dogs/test',
     target_size=(224, 224),
     batch_size=128,
     shuffle=True,
    classes=["."], #permet de considerer le path comme repertoire principale en l'abscence de sous repertoire
     class_mode='binary'
)

# 4
def plotImages(images_arr, probabilities = False):
    fig, axes = plt.subplots(len(images_arr), 1, figsize=(5,len(images_arr) * 3))
    if probabilities is False:
      for img, ax in zip( images_arr, axes):
          ax.imshow(img)
          ax.axis('off')
    else:
      for img, probability, ax in zip( images_arr, probabilities, axes):
          ax.imshow(img)
          ax.axis('off')
          if probability > 0.5:
              ax.set_title("%.2f" % (probability*100) + "% dog")
          else:
              ax.set_title("%.2f" % ((1-probability)*100) + "% cat")
    plt.show()

sample_training_images, _ = next(train_data_gen)
plotImages(sample_training_images[:5])

# 5
train_image_generator = ImageDataGenerator(
    rotation_range=40,
    zoom_range=0.1,
    vertical_flip=False,
    horizontal_flip = True,
    rescale=1./255.,
    width_shift_range =0.1,
    height_shift_range =0.1,
    shear_range=0.1,
    brightness_range = [0.8, 1],
    fill_mode="nearest")

# 6
train_data_gen = train_image_generator.flow_from_directory(batch_size=batch_size,
                                                     directory=train_dir,
                                                     target_size=(IMG_HEIGHT, IMG_WIDTH),
                                                     class_mode='binary')

augmented_images = [train_data_gen[0][0][0] for i in range(5)]
print(type(train_data_gen))
plotImages(augmented_images)

# 7 Definition du modèle avec 58% de précision

# model = Sequential(
#    [ tf.keras.layers.Conv2D(16, 3, activation = 'relu', input_shape = (150, 150, 3)),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Conv2D(32, 3, activation = 'relu'),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Conv2D(64, 3, activation = 'relu'),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Dropout(0.2),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(32, activation = 'relu'),
#     tf.keras.layers.Dense(32, activation = 'relu'),
#     tf.keras.layers.Dense(2, activation = 'softmax')]

# )

# model.compile( optimizer = 'adam',
#               loss = 'sparse_categorical_crossentropy',
#               metrics = ['accuracy']
# )

# model.summary()



# Geler les poids du modèle pré-entraîné par transfert learning 63%
base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

# # Créer le modèle séquentiel pour l'ajustement
model = Sequential([
    base_model,
    tf.keras.layers.GlobalAveragePooling2D(),
    Dense(256, activation='relu'),
    Dropout(0.5),
    Dense(2,activation='sigmoid')  # Utilisation de 'sigmoid' car il s'agit d'un problème de classification binaire
])

# # Compiler le modèle
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Afficher un résumé du modèle
model.summary()

from math import ceil

steps_per_epoch=ceil(len(train_data_gen)/batch_size)
steps_per_epoch

validation_steps = ceil(len(val_data_gen) / batch_size)
validation_steps

# 8
history = model.fit(
    train_data_gen, #generateur
    epochs=epochs,# episode
    validation_data=val_data_gen, # données de consideration
)

model.save('cat_detector_58.h5')

model.save('cat_detctor_63.keras')

# 9
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

predictions=model.predict(test_data_gen,verbose=1)
print(predictions)
probabilities = []
for a in predictions:
  if a[0] > a[1]:
    probabilities.append(0)
  else:
    probabilities.append(1)

print(len(probabilities))
print(type(probabilities))

sample_training_images, _ = next(test_data_gen)
print(probabilities)
plotImages(sample_training_images[:15], probabilities)
#0=chat et 1=chien

# 11
answers =  [1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0,
            1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0,
            1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
            1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1,
            0, 0, 0, 1, 0, 0]
print(len(answers))
correct = 0

for probability, answer in zip(probabilities, answers):
  if round(probability) == answer:
    correct +=1

percentage_identified = (correct / len(answers)) * 100

passed_challenge = percentage_identified >= 63

print(f"Your model correctly identified {round(percentage_identified, 2)}% of the images of cats and dogs.")

if passed_challenge:
  print("You passed the challenge!")
else:
  print("You haven't passed yet. Your model should identify at least 63% of the images. Keep trying. You will get it!")