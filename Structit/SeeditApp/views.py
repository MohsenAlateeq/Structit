from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from accounts.models import Profile
from .models import Project, App, Table
import requests
import re

def createApps(text: str):
    url = "https://experimental.willow.vectara.io/v1/completions"
    payload = {
        "model": "text-davinci-003",
        "prompt": text,
        "max_tokens": 500,
        "temperature": 0
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "customer-id": "1509971119",
        "x-api-key": ""
    }
    data: str = ''
    while not 'microservice.' in data.lower():
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()['choices'][0]['text']
    return re.compile('(?=[0-9].)').split(data)

def createColumns(text: str):
    url = "https://experimental.willow.vectara.io/v1/completions"

    payload = {
        "model": "text-davinci-003",
        "prompt": text,
        "max_tokens": 500,
        "temperature": 0
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        "customer-id": "1509971119",
        "x-api-key": ""
    }
    data: str = ''
    while not ('_id' and ': ') in data.lower():
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()['choices'][0]['text']
    return re.compile('(?=[0-9].)').split(data)



# Create your views here.
def homePage(request: HttpRequest):
    return render(request, 'SeeditApp/home.html')

def aboutPage(request: HttpRequest):
    '''Display about page.'''
    return render(request, 'SeeditApp/about.html')

def contactPage(request: HttpRequest):
    '''Display contact page.'''
    return render(request, 'SeeditApp/contact.html')

def profileDetail(request: HttpRequest, username: str):
    '''Return user profile'''
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    return render(request, 'SeeditApp/profile.html')

def editProfile(request: HttpRequest, username: str):
    '''Return user detail or accept user changes inputs.'''
    user: User = User.objects.get(username=username)
    profile: Profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        profile.name = request.POST['name']
        profile.bio = request.POST['bio']
        try:
            profile.image = request.FILES['image']
        except:
            profile.image = profile.image
        user.email = request.POST['email']
        if request.POST['password']:
            if request.POST['password'] == request.POST['confirm-password']:
                user.set_password(request.POST['password'])
                user.save()
                profile.save()
                return redirect('accounts:logout_page')
            else:
                password_message: str = 'Passwords not match.'
        else:
            user.password = user.password
        user.save()
        profile.save()
        return redirect('SeeditApp:profile_page', user.username)
            
    context: dict = {'user':user}
    return render(request, 'SeeditApp/edit_profile.html', context)

def addProject(request: HttpRequest):
    '''Add new opportunity'''
    user = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        text = f"If I want to make {request.POST['project_name']} application and there's microservices what will be those microservices, Give them to me in points each point starts only with microservice name followed of word (microservice) then dot."
        list_of_apps = createApps(text)
        the_project = Project.objects.create(name=request.POST['project_name'], profile=user_profile)
        the_project.save()
        for app in list_of_apps:
            if 'microservice' in app.lower():
                number_index = app.find('. ') + 2
                last_index_name = app.lower().find('microservice.')
                the_app = app.replace('\n', '')[number_index:last_index_name]
                App.objects.create(name=the_app, project=the_project)
        apps_list_sentece = ''
        apps_of_project = App.objects.filter(project=the_project)
        for app in apps_of_project:
            if app.name == apps_of_project.first().name: 
                apps_list_sentece += app.name + ', '
            elif app.name == apps_of_project.last().name:
                apps_list_sentece += 'and ' + app.name
            else:
                apps_list_sentece += app.name + ', '
        for microservice in apps_of_project:
            text = f"If I have {microservice.name} microservice in {the_project.name} application contains ({apps_list_sentece}) microservices, What columns should be in {microservice.name} microservice table, Give them to me in points each point starts only with column name followed of word (column), Then a colon followed of column type (Types can be Integer, String, Float, Boolean, Date, Time, File, Email, Password and Array) then dot."
            list_of_tables = createColumns(text)
            for table in list_of_tables:
                table = table.lower()
                if 'column:' in table:
                    table = table.replace(' column:', ':')
                    number_index = table.find('. ') + 2
                    end_column = table.find(': ')
                    column = table.replace('\n', '')[number_index:end_column]
                    type = table.replace('\n', '')[(end_column + 2):][:-1]
                    #if len(type) > 0 and len(type) < 20:
                    Table.objects.create(app=microservice, name=column, type=type, project=the_project)
        return redirect('SeeditApp:project_detail', project_id=the_project.id)
    return render(request, 'SeeditApp/add_project.html')

def displayProjects(request: HttpRequest):
    '''Display Latest Opportunities.'''
    context = {}
    return render(request, 'SeeditApp/projects.html', context)

def projectDetail(request: HttpRequest, project_id: int):
    '''Show opportunity details.'''
    project = Project.objects.get(id=project_id)
    apps = App.objects.filter(project_id=project_id)
    for app in apps:
        if Table.objects.filter(project_id=project_id, app_id=app.id).count() < 2:
            app.delete()
    apps = App.objects.filter(project_id=project_id)
    tables = Table.objects.filter(project_id=project_id)
    context = {'project':project, 'apps': apps, 'tables':tables}
    return render(request, 'SeeditApp/project_detail.html', context)
