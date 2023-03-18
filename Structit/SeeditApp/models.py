from django.db import models
from accounts.models import Profile
from datetime import datetime

# Create your models here.
class Project(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    documentation = models.TextField(max_length=512)


class App(models.Model):
    name = models.CharField(max_length=256)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class Table(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    type = models.CharField(max_length=256)

