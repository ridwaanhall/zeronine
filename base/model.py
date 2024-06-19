import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from scipy import ndimage

model_zeronine_en = tf.keras.models.load_model('model/zeronine_en.h5')
class_labels_en = ['eight', 'five', 'four', 'nine', 'one', 'seven', 'six', 'three', 'two', 'zero']

model_zeronine_ar = tf.keras.models.load_model('model/zeronine_ar.h5')

def predict_en(img):
    try:
        # Convert image to RGB if it has an alpha channel or is grayscale
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((150, 150))  # Ensure the size matches the model's expected input
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0  # Normalize the image

        prediction = model_zeronine_en.predict(img_tensor)
        probabilities = prediction[0]

        sorted_predictions = sorted(
            zip(class_labels_en, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_predictions
    except Exception as e:
        print(f"Error in predict_test: {e}")
        return []
    
def preprocess_image(img):
    """Preprocess the image to the format expected by the model."""
    img = img.convert('L')  # Convert image to grayscale
    img = img.resize((28, 28))  # Resize image to 28x28 pixels
    img_array = image.img_to_array(img)
    img_array = ndimage.rotate(img_array, -90)  # Rotate the image by -90 degrees to fix orientation
    img_array = np.fliplr(img_array)  # Flip the image horizontally to correct left-right orientation
    img_array = img_array.reshape((1, 784))  # Reshape to match model input
    img_array = img_array / 255.0  # Normalize the image
    return img_array

def predict_ar(img):
    """Predict the digit from the provided image and return probabilities."""
    processed_img = preprocess_image(img)
    prediction = model_zeronine_ar.predict(processed_img)
    probabilities = prediction[0]
    sorted_predictions = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
    return sorted_predictions