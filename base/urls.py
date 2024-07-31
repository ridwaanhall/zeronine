from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_en, name='redirect_to_en'),
    
    path('en/number', views.zeronine_en, name='ZeronineEN'),
    path('en/predict-number', views.predict_zeronine_en_num, name='PredictZeronineEN'),
    
    path('en/char', views.zeronine_en_char, name='ZeronineENChar'),
    path('en/predict-char', views.predict_zeronine_en_char, name='PredictZeronineENChar'),
    
    path('ar/number', views.zeronine_ar, name='ZeronineAR'),
    path('ar/predict-number', views.predict_zeronine_ar_num, name='PredictZeronineAR'),
    
    path('ar/char', views.zeronine_ar_char, name='ZeronineARChar'),
    path('ar/predict-char', views.predict_zeronine_ar_char, name='PredictZeronineARChar'),
]
