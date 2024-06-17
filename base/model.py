import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

# Load your model
model = tf.keras.models.load_model('zeronine.h5')

# Define a function to preprocess and predict
def predict_image(img_path):
    img = image.load_img(img_path, target_size=(150, 150))
    img_tensor = image.img_to_array(img)
    img_tensor = np.expand_dims(img_tensor, axis=0)
    img_tensor /= 255.

    prediction = model.predict(img_tensor)
    prediction_probabilities = prediction[0]
    sorted_indices = np.argsort(prediction_probabilities)[::-1]

    labels = ['eight', 'five', 'four', 'nine', 'one', 'seven', 'six', 'three', 'two', 'zero']
    sorted_labels = [(labels[i], prediction_probabilities[i]) for i in sorted_indices]

    return sorted_labels
