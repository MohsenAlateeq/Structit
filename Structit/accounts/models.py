from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=128)
    bio = models.TextField()
    user_roles_choices = models.TextChoices('User Role', ['Entreprenuer', 'Investor', 'Expert'])
    user_role = models.CharField(max_length=64, choices=user_roles_choices.choices, default=user_roles_choices.Entreprenuer)
    image = models.ImageField(upload_to='images/users/', default='images/users/user.png')
