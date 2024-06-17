from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .model import predict_image

def index(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        img_path = fs.save(uploaded_file.name, uploaded_file)
        img_url = fs.url(img_path)
        
        sorted_predictions = predict_image(fs.path(img_path))

        return render(request, 'base/index.html', {
            'img_url': img_url,
            'sorted_predictions': sorted_predictions
        })
    
    return render(request, 'base/index.html')
