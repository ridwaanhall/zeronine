import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf

model_zeronine = tf.keras.models.load_model('model/zeronine.h5')
class_labels = ['eight', 'five', 'four', 'nine', 'one', 'seven', 'six', 'three', 'two', 'zero']

def predict(img):
    try:
        # Convert image to RGB if it has an alpha channel or is grayscale
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((150, 150))  # Ensure the size matches the model's expected input
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0  # Normalize the image

        prediction = model_zeronine.predict(img_tensor)
        probabilities = prediction[0]

        sorted_predictions = sorted(
            zip(class_labels, probabilities),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_predictions
    except Exception as e:
        print(f"Error in predict_test: {e}")
        return []