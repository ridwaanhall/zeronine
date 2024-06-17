from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import io
from .model import predict

def index(request):
    return render(request, 'base/index.html')

def predict_view(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_file = request.FILES['image']

        image_content = uploaded_file.read()
        image_file = io.BytesIO(image_content)

        img = Image.open(image_file)
        sorted_predictions = predict(img)

        # Convert float32 to float
        sorted_predictions = [(label, float(probability)) for label, probability in sorted_predictions]

        return JsonResponse({
            'sorted_predictions': sorted_predictions
        })
    return JsonResponse({
        'error': 'Invalid request'
    }, status=400)
