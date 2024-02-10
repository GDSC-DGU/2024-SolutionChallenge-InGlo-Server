from django.db import models
from django.conf import settings
from sketches.models import Sketch

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    sketch = models.ForeignKey(Sketch, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    sdgs = models.IntegerField() # 반정규화. Sdgs 번호
    created_at = models.DateTimeField(auto_now_add=True)

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField()
    parent_feedback = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
