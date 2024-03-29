from django.db import models
from django.conf import settings

class Issue(models.Model):
    link = models.URLField(max_length=500)
    writer = models.CharField(max_length=500, blank=True, null=True, default='unknown')
    title = models.CharField(max_length=500)
    content = models.TextField()
    image_url = models.URLField(max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

class IssueList(models.Model):
    issue = models.OneToOneField(Issue, on_delete=models.CASCADE, related_name='list')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    country = models.CharField(max_length=100)
    sdgs = models.IntegerField() # SDGs 번호로
    image_url = models.URLField(max_length=1000,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

class IssueComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.content}"

class IssueLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)