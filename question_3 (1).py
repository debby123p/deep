# -*- coding: utf-8 -*-
"""question 3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CWD1u0niRWx7W_6wXONqjI5Ow8ztrrBP
"""

import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import numpy as np

def create_dense_network(input_shape, num_classes, hidden_layers, activation_functions):
    model = models.Sequential()
    model.add(layers.Flatten(input_shape=input_shape))
    for neurons, activation in zip(hidden_layers, activation_functions):
        model.add(layers.Dense(neurons, activation=activation))
    model.add(layers.Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# Load and preprocess the MNIST dataset
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.astype('float32') / 255
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels, 10)
test_labels = to_categorical(test_labels, 10)

# Hyperparameter sets for tuning
hyperparameters = [
    {'batch_size': 128, 'epochs': 10, 'hidden_layers': [512], 'activation_functions': ['relu']},
    {'batch_size': 128, 'epochs': 20, 'hidden_layers': [512, 256], 'activation_functions': ['relu', 'relu']}
]

# Placeholder for the best model's validation accuracy and configuration
best_val_accuracy = 0
best_config = None
final_model = None

for config in hyperparameters:
    model = create_dense_network(input_shape=(28, 28), num_classes=10,
                                 hidden_layers=config['hidden_layers'],
                                 activation_functions=config['activation_functions'])
    history = model.fit(train_images, train_labels,
                        epochs=config['epochs'],
                        batch_size=config['batch_size'],
                        validation_split=0.2,
                        verbose=0)

    val_accuracy = max(history.history['val_accuracy'])
    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        best_config = config
        final_model = model  # Update the final_model with the current best model

print(f"Best Validation Accuracy: {best_val_accuracy}")
print(f"Best Configuration: {best_config}")

# Correctly evaluate the final model on the test data
if final_model is not None:
    test_loss, test_acc = final_model.evaluate(test_images, test_labels, verbose=0)
    print(f"Test accuracy with best configuration: {test_acc}")
else:
    print("No model was trained.")

