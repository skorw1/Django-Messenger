from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()

