from django.urls import path
from . import views
from . import api_views

urlpatterns = [

# model signals
    path('', views.student_list, name='student_list'),
    path('create/', views.student_create, name='student_create'),
    path('update/<int:pk>/', views.student_update, name='student_update'),
    path('delete/<int:pk>/', views.student_delete, name='student_delete'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('logging/',views.my_view, name='logging'),





# api functions
# model signals
    path('students/', api_views.StudentListCreateAPIView.as_view(), name='student_api_list_create'),
    path('students/<int:pk>/', api_views.StudentRetrieveUpdateDestroyAPIView.as_view(), name='student_api_detail'),


]
