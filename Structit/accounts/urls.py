from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.registerPage, name='register_page'),
    path('login/', views.loginPage, name='login_page'),
    path('logout/', views.logoutPage, name='logout_page')
]