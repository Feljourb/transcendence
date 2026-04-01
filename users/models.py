from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True) 
    location = models.CharField(max_length=30, blank=True) 
    skills = models.CharField(max_length=255, blank=True, help_text="List your skills separated by commas") 
    avatar = models.ImageField(upload_to='avatars/',default='avatars/default.png', null=True, blank=True) 

    def __str__(self):
        return self.username 

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE) 
    reciever = models.ForeignKey(User, related_name='recieved_requests', on_delete=models.CASCADE) 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ] 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending') 
    created_at = models.DateTimeField(auto_now_add=True) 
    class Meta:
        unique_together = ('sender', 'reciever') 

    def __str__(self):
        return f"{self.sender}->{self.reciever} ({self.status})" 
