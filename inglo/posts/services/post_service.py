from django.db.models import Q
from ..models import Post, Sketch, Feedback, PostLike
from django.db import transaction

class PostService:

    @staticmethod
    def get_post_list(content='', username=''):
        queryset = Post.objects.all()
        if content:
            queryset = queryset.filter(content__icontains=content)
        if username:
            queryset = queryset.filter(user__username__icontains=username)
        return queryset
    
    @staticmethod    
    def get_post_by_id(post_id):
        return Post.objects.get(id=post_id)

    @staticmethod
    @transaction.atomic
    def create_post(user, sketch_id, title, content, sdgs):
        try:
            sketch = Sketch.objects.get(id=sketch_id)
            post = Post.objects.create(user=user, sketch=sketch,title=title, content=content, sdgs=sdgs)
            return post
        except (ValueError, TypeError):
            return None
        
    @staticmethod
    @transaction.atomic
    def update_post(user, post_id, content):
        post = Post.objects.get(id=post_id)
        if post.user != user:
            return None
        post.content = content
        post.save()
        return post
    
    @staticmethod
    @transaction.atomic
    def delete_post(user, post_id):
        post = Post.objects.get(id=post_id)
        if post.user != user:
            return None
        post.delete()
        return post
    
    @staticmethod
    @transaction.atomic
    def toggle_like(user, post_id):
        post = Post.objects.get(id=post_id)
        post_like, created = PostLike.objects.get_or_create(user=user, post_id=post_id)
        if not created:
            post_like.delete()
            post_like.update(like_count=F('like_count') - 1)
            return False
        else:
            post_like.update(like_count=F('like_count') + 1)
            return True