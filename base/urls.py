from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_en, name='redirect_to_en'),
    
    path('en/', views.zeronine_en, name='ZeronineEN'),
    path('en/predict/', views.predict_zeronine_en, name='PredictZeronineEN'),
    
    path('ar/', views.zeronine_ar, name='ZeronineAR'),
    path('ar/predict/', views.predict_zeronine_ar, name='PredictZeronineAR'),
]
