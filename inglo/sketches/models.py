from django.db import models
from django.conf import settings

class Problem(models.Model):
    content = models.TextField()
    sdgs = models.IntegerField()

class Sketch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sketches')
    title = models.CharField(max_length=255)
    description = models.TextField()
    content = models.TextField()
    image_url = models.URLField()
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, related_name='sketches')
    hmw = models.ForeignKey('HMW', on_delete=models.SET_NULL, null=True, related_name='sketches')
    crazy8stack = models.ForeignKey('Crazy8Stack', on_delete=models.SET_NULL, null=True, related_name='sketches')
    created_at = models.DateTimeField(auto_now_add=True)

class HMW(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hmws')
    content = models.TextField()

class Crazy8Stack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='crazy8stacks')

class Crazy8Content(models.Model):
    crazy8stack = models.ForeignKey(Crazy8Stack, on_delete=models.CASCADE, related_name='contents')
    content = models.TextField()
    vote_count = models.IntegerField(default=0)
