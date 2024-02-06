from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    #username, email, first_name, last_name, password 포함
    country = models.CharField(max_length=100)
    language = models.CharField(max_length=50)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    liked_total = models.IntegerField(default=0)
    sketch_num = models.IntegerField(default=0)
    feedback_total = models.IntegerField(default=0)