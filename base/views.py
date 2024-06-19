from django.shortcuts import render, redirect
from django.http import JsonResponse
from PIL import Image
import base64
import io
import json
from .model import predict_en, predict_ar

def redirect_to_en(request):
    return redirect('ZeronineEN')

# digits
def zeronine_en(request):
    return render(request, 'base/zeronine-en.html')

def zeronine_ar(request):
    return render(request, 'base/zeronine-ar.html')

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

def predict_zeronine_en(request):
    return predict_image(request, predict_en)

def predict_zeronine_ar(request):
    return predict_image(request, predict_ar)
