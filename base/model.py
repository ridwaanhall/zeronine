import numpy as np
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from scipy import ndimage


# class_labels_en = ['eight', 'five', 'four', 'nine', 'one', 'seven', 'six', 'three', 'two', 'zero']
# model
model_zeronine_en_num = tf.keras.models.load_model('model/zeronine_en_num.h5')
model_zeronine_ar_num = tf.keras.models.load_model('model/zeronine_ar_num.h5')
model_zeronine_ar_char = tf.keras.models.load_model('model/zeronine_ar_char.h5')


# class labels
class_labels_en = ['8', '5', '4', '9', '1', '7', '6', '3', '2', '0']

class ArabicLabelHandler:
    def __init__(self):
        self.labels = {
            1: "Alef (أ)", 2: "Bah (ب)", 3: "Teh (ت)", 4: "Theh (ث)", 5: "Jeem (ج)", 6: "Hah (ح)",
            7: "Khah (خ)", 8: "Dal (د)", 9: "Thal (ذ)", 10: "Reh (ر)", 11: "Zay (ز)", 12: "Seen (س)",
            13: "Sheen (ش)", 14: "Sad (ص)", 15: "Dad (ض)", 16: "Tah (ط)", 17: "Zah (ظ)", 18: "Ain (ع)",
            19: "Ghain (غ)", 20: "Feh (ف)", 21: "Qaf (ق)", 22: "Kaf (ك)", 23: "Lam (ل)", 24: "Meem (م)",
            25: "Noon (ن)", 26: "Heh (هـ)", 27: "Waw (و)", 28: "Yeh (ي)"
        }

    def get_label(self, class_number):
        return self.labels.get(class_number, "Unknown")

    def get_num_classes(self):
        return len(self.labels)

# Preprocess Image
def preprocess_image_ar_num(img):
    """Preprocess the image to the format expected by the model."""
    img = img.convert('L')  # Convert image to grayscale
    img = img.resize((28, 28))  # Resize image to 28x28 pixels
    img_array = image.img_to_array(img)
    img_array = ndimage.rotate(img_array, -90)  # Rotate the image by -90 degrees to fix orientation
    img_array = np.fliplr(img_array)  # Flip the image horizontally to correct left-right orientation
    img_array = img_array.reshape((1, 784))  # Reshape to match model input
    img_array = img_array / 255.0  # Normalize the image
    return img_array

def preprocess_image_ar_char(img):
    """Preprocess the image to the format expected by the model."""
    img = img.convert('L')  # Convert image to grayscale
    img = img.resize((32, 32))  # Resize image to 32x32 pixels
    img_array = image.img_to_array(img)
    img_array = ndimage.rotate(img_array, -90)  # Rotate the image by -90 degrees to fix orientation
    img_array = np.fliplr(img_array)  # Flip the image horizontally to correct left-right orientation
    img_array = img_array.reshape((1, 1024))  # Reshape to match model input
    img_array = img_array / 255.0  # Normalize the image
    return img_array


# predict
def predict_en_num(img):
    try:
        # Convert image to RGB if it has an alpha channel or is grayscale
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        img = img.resize((150, 150))  # Ensure the size matches the model's expected input
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0)
        img_tensor /= 255.0  # Normalize the image

        prediction = model_zeronine_en_num.predict(img_tensor)
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

def predict_ar_num(img):
    """Predict the digit from the provided image and return probabilities."""
    processed_img = preprocess_image_ar_num(img)
    prediction = model_zeronine_ar_num.predict(processed_img)
    probabilities = prediction[0]
    sorted_predictions = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
    return sorted_predictions

def predict_ar_char(img):
    """Predict the Arabic character from the provided image and return the predictions with labels."""
    label_handler = ArabicLabelHandler()
    processed_img = preprocess_image_ar_char(img)
    prediction = model_zeronine_ar_char.predict(processed_img)
    probabilities = prediction[0]
    sorted_predictions = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
    sorted_predictions = [(label_handler.get_label(idx), prob) for idx, prob in sorted_predictions]
    return sorted_predictions
