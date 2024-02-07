from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    #username, email, first_name, last_name, password 포함
    #username은 unique함. 고유한 닉네임으로 사용할 수 있음
    social_id = models.CharField(max_length=255, blank=True, null=True)
    country = models.IntegerField() # 국가 번호로
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    liked_total = models.IntegerField(default=0)
    sketch_num = models.IntegerField(default=0)
    feedback_total = models.IntegerField(default=0)