from ..models import Sketch
from ..models import Problem
from dotenv import load_dotenv
import requests
from io import BytesIO
import os
import boto3
import magic
from urllib.parse import urlparse

class SketchService:
    def get_sketches_by_user(user):
        return Sketch.objects.filter(user=user)
    
    def update_sketch(user,problem_id,title,description,image,content):
        problem = Problem.objects.get(id = problem_id)
        sketch = Sketch.objects.filter(user=user, problem=problem).order_by('-created_at').first()

        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        file_path = f'user_{user.id}/sketch_{sketch.id}'  # S3 내에서 파일을 저장할 경로

        mime_type = magic.from_buffer(image.read(2048), mime=True)
        image.seek(0)  

        s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ContentType=mime_type)

        image_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}"

        sketch.title = title
        sketch.description = description
        sketch.image_url = image_url
        sketch.content = content
        sketch.save()
        return sketch
    
    def delete_sketch(sketch_id):
        sketch = Sketch.objects.get(id=sketch_id)
        sketch.delete()
        return sketch

    def get_sketch_by_id(sketch_id):
        return Sketch.objects.get(id=sketch_id)