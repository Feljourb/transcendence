from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True) 
    location = models.CharField(max_length=30, blank=True) 
    skills = models.CharField(max_length=255, blank=True, help_text="List your skills separated by commas") 

    def __str__(self):
        return self.username