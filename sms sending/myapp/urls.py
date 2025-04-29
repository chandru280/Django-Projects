from django.urls import path
from . import views

urlpatterns = [
    path('send/', views.send_whatsapp, name='send_whatsapp'),
    path('send_sms/', views.send_sms, name='send_sms'),
    path('whatsapp/', views.incoming_message, name='incoming_message'),

     path('send-message/', views.send_message_view, name='send_message'),

]
