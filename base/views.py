from django.shortcuts import render, redirect
from django.http import JsonResponse
from PIL import Image
import base64
import io
import json
from .model import predict_en_num, predict_ar_num, predict_ar_char, predict_en_char

def redirect_to_en(request):
    return redirect('ZeronineEN')

# digits
def zeronine_en(request):
    return render(request, 'base/zeronine-en.html')

def zeronine_ar(request):
    return render(request, 'base/zeronine-ar.html')

# characters
def zeronine_ar_char(request):
    return render(request, 'base/zeronine-ar-char.html')

def zeronine_en_char(request):
    return render(request, 'base/zeronine-en-char.html')

def process_image(request):
    if 'image' in request.FILES:
        uploaded_file = request.FILES['image']
        image_content = uploaded_file.read()
    else:
        data = json.loads(request.body.decode('utf-8'))
        image_data = data.get('image').split(',')[1]
        image_content = base64.b64decode(image_data)
        
    image_file = io.BytesIO(image_content)
    return Image.open(image_file)

def predict_image(request, prediction_function):
    '''Predict the digit from the provided image and return probabilities.'''
    if request.method == 'POST':
        try:
            img = process_image(request)
            sorted_predictions = prediction_function(img)

            if not sorted_predictions:
                return JsonResponse({'error': 'Prediction failed'}, status=500)

            sorted_predictions = [(label, float(probability)) for label, probability in sorted_predictions]
            return JsonResponse({'sorted_predictions': sorted_predictions})
        except Exception as e:
            print(f"Error in prediction: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

# digits
def predict_zeronine_en_num(request):
    return predict_image(request, predict_en_num)

def predict_zeronine_ar_num(request):
    return predict_image(request, predict_ar_num)

# characters
def predict_zeronine_ar_char(request):
    return predict_image(request, predict_ar_char)

def predict_zeronine_en_char(request):
    return predict_image(request, predict_en_char)