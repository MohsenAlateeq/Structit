from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Profile

# Create your views here.
def registerPage(request: HttpRequest):
    '''Allow vistiors to register.'''
    user_roles = Profile.user_roles_choices.choices
    if request.method == 'POST':
        username: str = request.POST['username'].lower()
        try:
            if request.POST['password'] == request.POST['confirm-password']:
                user = User.objects.create_user(username=username, email=request.POST['email'], password=request.POST['password'])
                profile = Profile(user=user, bio='', user_role=request.POST['user_role'])
                profile.save()
                return redirect('accounts:login_page')
            else:
                password_error_message: str = "Passwords not match"
        except:
            error_message: str = 'User exist'
    context: dict = {'user_roles':user_roles}
    return render(request, 'accounts/register.html', context)

def loginPage(request: HttpRequest):
    '''Allow users to login with their credintals.'''
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user:
            login(request, user)
            return redirect('SeeditApp:home_page')
        else:
            error_message: str = 'User or password error!'
    return render(request, 'accounts/login.html')

def logoutPage(request: HttpRequest):
    '''Logout user and remove the session'''
    logout(request)
    return render(request, 'accounts/logout.html')