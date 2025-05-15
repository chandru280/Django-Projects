from django.urls import path
from .views import *

urlpatterns = [
    path('', generate_qr, name='generate_qr'),
    path('datas/', generate_qr2, name='generate_qr'),
    path('link/', generate_qr2, name='generate_qr'),
    path('qr/<int:pk>/', qr_detail, name='qr_detail'),
]
