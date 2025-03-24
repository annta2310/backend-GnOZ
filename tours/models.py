from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('AGENT', 'Agent'),
        ('MANAGER', 'Manager'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='AGENT')
    
    def is_admin(self):
        return self.user_type == 'ADMIN'
    
    def is_agent(self):
        return self.user_type == 'AGENT'
    
    def is_manager(self):
        return self.user_type == 'MANAGER'

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    profile_pic = models.ImageField(upload_to='agent_pics/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_absolute_url(self):
        return reverse('agent-detail', kwargs={'pk': self.pk})

class Tour(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tours')
    total_seats = models.PositiveIntegerField(default=10)
    available_seats = models.PositiveIntegerField(default=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('tour-detail', kwargs={'pk': self.pk})