from django.urls import path 
from packageapp import views  

urlpatterns = [
    path('person/create/', views.create_person, name='create_person'),
    path('person/update/<int:pk>/', views.update_person, name='update_person'),
    path('people/', views.person_list_view, name='person-list'),
    path('update/<int:pk>/', views.update_person, name='update_person'),
    path('delete/<int:pk>/', views.delete_person, name='delete_person'),


    path('people_list/', views.person_list_pagenation, name='person_list'),

]
