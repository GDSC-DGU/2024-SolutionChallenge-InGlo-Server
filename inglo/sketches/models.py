from django.db import models
from django.conf import settings

class Problem(models.Model):
    content = models.TextField()
    sdgs = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.content}"


class Sketch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sketches', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    problem = models.ForeignKey(Problem, on_delete=models.SET_NULL, null=True, related_name='sketches', blank=True)
    hmw = models.ForeignKey('HMW', on_delete=models.SET_NULL, null=True, related_name='sketches', blank=True)
    crazy8stack = models.ForeignKey('Crazy8Stack', on_delete=models.SET_NULL, null=True, related_name='sketches', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"


class HMW(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='hmws')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.content}"

class Crazy8Stack(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='crazy8stacks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - Crazy8Stack for {self.problem}'

class Crazy8Content(models.Model):
    crazy8stack = models.ForeignKey(Crazy8Stack, on_delete=models.CASCADE, related_name='contents')
    content = models.TextField()
    vote_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.content}"


class Crazy8Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    crazy8content = models.ForeignKey(Crazy8Content, on_delete=models.CASCADE, related_name='votes')
    created_at = models.DateTimeField(auto_now_add=True)