import tensorflow as tf
from tensorflow import keras
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
import os

# Load data from folders
root_dir = 'training_samples'
classes = [f for f in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, f))]

images = []
labels = []

for class_dir in classes:
    class_dir_path = os.path.join(root_dir, class_dir)
    for file in os.listdir(class_dir_path):
        img = keras.preprocessing.image.load_img(os.path.join(class_dir_path, file), target_size=(224, 224))
        img_array = keras.preprocessing.image.img_to_array(img)
        images.append(img_array)
        labels.append(classes.index(class_dir))

# Convert lists to numpy arrays
images = np.array(images)
labels = np.array(labels)

# One-hot encode labels
num_classes = len(classes)
labels_onehot = keras.utils.to_categorical(labels, num_classes)

# Split data into training and validation sets
train_images, val_images, train_labels, val_labels = train_test_split(images, labels_onehot, test_size=0.2, random_state=42)

# Normalize pixel values
train_images = train_images / 255.0
val_images = val_images / 255.0

# Define the CNN model architecture
model = keras.Sequential([
    keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(64, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Conv2D(128, (3, 3), activation='relu'),
    keras.layers.MaxPooling2D((2, 2)),
    keras.layers.Flatten(),
    keras.layers.Dense(128, activation='relu'),
    keras.layers.Dense(num_classes, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(train_images, train_labels, epochs=10, validation_data=(val_images, val_labels))
model.save('multiclass_model.h5')