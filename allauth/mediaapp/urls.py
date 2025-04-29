from django.urls import path
from . import views

urlpatterns = [
    path('accounts/login/', views.custom_login_view, name='account_login'),
    path('accounts/signup/', views.custom_signup_view, name='account_signup'),  # Overriding the allauth signup
    path('accounts/password_reset/', views.custom_password_reset_view, name='password_reset'),
    path('accounts/password_change/', views.custom_change_password_view, name='password_change'),
    path('accounts/change_email/', views.custom_change_email_view, name='change_email'),
    path('accounts/logout/', views.custom_logout_view, name='account_logout'),





]
