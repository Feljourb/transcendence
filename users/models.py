from django.db import models
from django.contrib.auth.models import AbstractUser

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True) 
    location = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.username
