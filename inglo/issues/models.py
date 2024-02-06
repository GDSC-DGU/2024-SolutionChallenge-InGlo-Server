from django.db import models
from users.models import User

class Issue(models.Model):
    link = models.URLField()
    writer = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

class IssueList(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name='list')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class IssueComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
