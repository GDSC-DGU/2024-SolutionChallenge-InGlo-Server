from django.contrib import admin
from .models import Post, Feedback, PostLike

admin.site.register(Post)
admin.site.register(Feedback)
admin.site.register(PostLike)
