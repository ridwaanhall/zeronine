from django.urls import path
from . import views

urlpatterns = [
    path('', views.zeronine_en, name='ZeronineEN'),
    path('predict/', views.predict_view, name='PredictZeronineEN'),
]
