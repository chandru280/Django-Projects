from django.urls import path
from .views import *


urlpatterns = [
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/queries/', BookQueryView.as_view(), name='book_queries'),
]
