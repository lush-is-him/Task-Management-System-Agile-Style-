# authentication/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # URL for login page
    path('logout/', views.user_logout, name='logout'),  # URL for logout
    path('register/', views.user_register, name='register'),  # URL for registration
]
