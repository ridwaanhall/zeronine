from django.shortcuts import render
from django.http import JsonResponse
from PIL import Image
import base64
import io
import json
from .model import predict

def index(request):
    return render(request, 'base/index.html')

def predict_view(request):
    if request.method == 'POST':
        try:
            if 'image' in request.FILES:
                uploaded_file = request.FILES['image']
                image_content = uploaded_file.read()
                image_file = io.BytesIO(image_content)
                img = Image.open(image_file)
            else:
                data = json.loads(request.body.decode('utf-8'))
                image_data = data.get('image').split(',')[1]
                image_content = base64.b64decode(image_data)
                image_file = io.BytesIO(image_content)
                img = Image.open(image_file)

            sorted_predictions = predict(img)

            if not sorted_predictions:
                return JsonResponse({'error': 'Prediction failed'}, status=500)

            sorted_predictions = [(label, float(probability)) for label, probability in sorted_predictions]

            return JsonResponse({'sorted_predictions': sorted_predictions})
        except Exception as e:
            print(f"Error in predict_view_test: {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
