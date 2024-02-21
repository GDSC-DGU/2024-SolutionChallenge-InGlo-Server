from ..models import Post, Sketch, PostLike
from django.db import transaction
from django.db.models import F
from django.http import Http404, HttpResponseBadRequest as Http400

class PostService:

    @staticmethod
    def get_post_list(content='', username=''):
        try:
            queryset = Post.objects.all()
            if content:
                queryset = queryset.filter(content__icontains=content)
            if username:
                queryset = queryset.filter(user__username__icontains=username)
            return queryset
        except Post.DoesNotExist:
            return Post.objects.none()
    
    @staticmethod    
    def get_post_by_id(post_id):
        try:
            post = Post.objects.get(id=post_id)
            return post
        except Post.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_post(user, sketch_id, title , content, sdgs):
        try:
            sketch = Sketch.objects.get(id=sketch_id)
            post = Post.objects.create(user=user, sketch=sketch,title=title, content=content, sdgs=sdgs)
            user.post_total += 1
            user.save()
            return post
        except (ValueError, TypeError, Sketch.DoesNotExist):
            return None
        
    @staticmethod
    @transaction.atomic
    def update_post(user, post_id, title, content):
        try:
            post = Post.objects.get(id=post_id)
            if post.user != user:
                return None
            post.content = content
            post.title = title
            post.save()
            return post
        except Post.DoesNotExist:
            return Http400("Post does not exist")
    
    @staticmethod
    @transaction.atomic
    def delete_post(user, post_id):
        try:
            post = Post.objects.get(id=post_id)
            if post.user != user:
                return None
            post.delete()
            return post
        except Post.DoesNotExist:
            return Http400("Post does not exist")
    
    @staticmethod
    @transaction.atomic
    def toggle_like(user, post_id):
        try:
            post = Post.objects.get(id=post_id)
            post_like, created = PostLike.objects.get_or_create(user=user, post_id=post_id)
            if not created:
                post_like.delete()
                post.likes = F('likes') - 1 
                post.save()
                return False
            else:
                post.likes = F('likes') + 1
                post.save()
                return True
        except Post.DoesNotExist:
            return None