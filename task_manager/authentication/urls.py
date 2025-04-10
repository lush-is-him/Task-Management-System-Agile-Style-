# authentication/urls.py
from django.urls import path
from . import views  # Import your views

urlpatterns = [
    path('login/', views.user_login, name='login'),  # URL for login page
    path('logout/', views.user_logout, name='logout'),  # URL for logout
    path('register/', views.user_register, name='register'),# URL for registration
    path("dashboard/", views.dashboard, name="dashboard"),  # Add this for da
    path('add-task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update_task/<int:task_id>/', views.update_task, name='update_task'),
     path('create_team/', views.create_team, name='create_team'),
    path('team/<int:team_id>/members/', views.view_team_members, name='view_team_members'),
    path('edit_team/<int:team_id>/', views.edit_team, name='edit_team'),
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'),
    path('add_member/<int:team_id>/', views.add_member, name='add_member'),


]
