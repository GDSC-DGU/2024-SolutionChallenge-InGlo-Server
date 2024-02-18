from django.db.models import Q
from ..models import Post, Sketch, Feedback, PostLike
from django.db import transaction
from django.db.models import F
import boto3
import os
import magic
from dotenv import load_dotenv

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
    def create_post(user, sketch_id, title, image , content, sdgs):
        try:
            sketch = Sketch.objects.get(id=sketch_id)
            post = Post.objects.create(user=user, sketch=sketch,title=title, content=content, sdgs=sdgs)
            user.post_total += 1
            user.save()

            s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

            file_path = f'user_{user.id}/post_{post.id}'  # S3 내에서 파일을 저장할 경로

            mime_type = magic.from_buffer(image.read(2048), mime=True)
            image.seek(0)  

            s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ContentType=mime_type)

            image_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}"
            post.image_url = image_url
            post.save()
            return post
        except (ValueError, TypeError):
            return None
        
    @staticmethod
    @transaction.atomic
    def update_post(user, post_id, title, content, image):
        post = Post.objects.get(id=post_id)
        if post.user != user:
            return None
        if image is not None:
            s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
            file_path = f'user_{user.id}/post_{post_id}'
            mime_type = magic.from_buffer(image.read(2048), mime=True)
            image.seek(0)
            s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ContentType=mime_type)
            image_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}"
            post.image_url = image_url
        
        post.content = content
        post.title = title
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
            post.likes = F('likes') - 1 
            post.save()
            return False
        else:
            post.likes = F('likes') + 1
            post.save()
            return True