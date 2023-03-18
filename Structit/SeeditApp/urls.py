from django.urls import path 
from . import views

app_name = 'SeeditApp'

urlpatterns = [
    path('', views.homePage, name='home_page'),
    path('about/', views.aboutPage, name='about_page'),
    path('contact/', views.contactPage, name='contact_page'),
    path('profile/<str:username>', views.profileDetail, name='profile_page'),
    path('profile/edit/<str:username>', views.editProfile, name='edit_profile_page'),
    path('dashboard/', views.displayProjects, name='projects_page'),
    path('projects/add/', views.addProject, name='create_project'),
    path('project/<int:project_id>/', views.projectDetail, name='project_detail'),
]