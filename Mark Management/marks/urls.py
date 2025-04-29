from django.urls import path 
from marks import views
from django.views.generic import TemplateView 
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', views.home, name='home'),
    path('academicyear', views.academicyear, name='academicyear'),

#Authendication
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('manage-permissions/', views.manage_user_permissions, name='manage_user_permissions'),


#Standard
    path('standard/create/', views.add_or_update_standard, name='create_standard'),
    path('standard/delete/<int:standard_id>/', views.delete_standard, name='delete_standard'),
    path('standard_list/', views.standard_list, name='standard_list'),
    path('standards/edit/<int:pk>/', views.edit_standard, name='edit_standard'),


#Subject
    path('subject_list/<int:standard_id>/', views.subject_list_standard, name='subject_list_standard'), # subject list based on Standard
    path('subject/delete/<int:subject_id>/from/<int:standard_id>/', views.delete_subject, name='delete_subject'),
    path('subjects/', views.subject_list, name='subject_list'),
    path('subjects/edit/<int:pk>/', views.edit_subject, name='edit_subject'),
    path('subjects/delete/<int:id>/', views.subject_delete, name='subject_delete'), # delete in subect list

   
#Test
    path('create_testname/', views.create_testname_with_subjects, name='create_testname_with_subjects'),
    path('fetch_subjects/', views.fetch_subjects, name='fetch_subjects'),

#Mark
    path('create_marks/<int:student_id>/', views.create_marks, name='create_marks'),
    path('ajax/get-subjects/', views.get_subjects, name='get_subjects'),
    path('update_mark/<int:mark_id>/', views.update_mark, name='update_mark'),
    path('delete_mark/<int:id>/', views.mark_delete, name='delete_mark'),
    

   

#Student
    path('students/<int:standard_id>', views.student_list, name='student_list'),
    path('student/<int:student_id>/', views.student_detail, name='student_detail'),
    path('student_add/', views.add_student, name='add_student'),
    path('student/<int:student_id>/<int:standard_id>/update/', views.update_student, name='update_student'),
    path('student/<int:student_id>/<int:standard_id>/delete/', views.delete_student, name='delete_student'),
   
    path('generate_register_numbers/<int:standard_id>/', views.generate_register_numbers, name='generate_register_numbers'),

#Staff
    path('add_staff/', views.staff_add, name='staff_add'),
    path('list_staff/', views.staff_list, name='staff_list'),
    path('<int:staff_id>/detail/', views.staff_detail, name='staff_detail'),
    path('<int:staff_id>/update/', views.staff_update, name='staff_update'),
    path('<int:staff_id>/delete/', views.staff_delete, name='staff_delete'),


 
   

# Student Profile(Dashboard)
    path('<int:id>/student', views.stu_profile, name='student_profile'),  


    ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)