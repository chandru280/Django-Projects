from django.urls import path
from .views import *


urlpatterns = [
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/queries/', BookQueryView.as_view(), name='book_queries'),

    
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    ]

