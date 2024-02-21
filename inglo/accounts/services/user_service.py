from django.db import transaction
import boto3
import os
import magic

class UserService:

    @staticmethod
    @transaction.atomic
    def update_user_profile_image(user, image):
        s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        file_path = f'user_{user.id}/{image.name}'  # S3 내에서 파일을 저장할 경로

        mime_type = magic.from_buffer(image.read(2048), mime=True)
        image.seek(0)  

        s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ContentType=mime_type)

        image_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}"
        user.profile_img = image_url
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def update_global_impact(user):
        global_impact = (user.liked_total + user.sketch_num*7 + user.post_total*7 + user.feedback_total*3)/10
        if global_impact > 100:
            user.global_impact = 100
        user.global_impact = global_impact
        user.save()

    @staticmethod
    @transaction.atomic
    def update_user_info(user, name, country, language):
        user.name = name
        user.country = country
        user.language = language
        user.additional_info_provided = True
        user.save()
        return user