from django.db import models
from users.models import User

class Problem(models.Model):
    content = models.TextField()
    sdgs = models.CharField(max_length=100)
    # SDGs 관계는 core 앱에서 정의

class Sketch(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sketches')
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image_url = models.URLField()
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, related_name='sketches')
    created_at = models.DateTimeField(auto_now_add=True)

class HMW(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hmws')
    content = models.TextField()

class Crazy8Stack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='crazy8stacks')

class Crazy8Content(models.Model):
    crazy8stack = models.ForeignKey(Crazy8Stack, on_delete=models.CASCADE, related_name='contents')
    content = models.TextField()
