from django.db.models import F
from django.db import transaction
from django.db.models import ExpressionWrapper, fields
from django.utils import timezone
from ..models import Issue, IssueList, IssueLike
from datetime import timedelta
from ..utils.classifier import classify_news
from ..utils.news_api import fetch_news
from dotenv import load_dotenv
import requests
from io import BytesIO
import os
import boto3
import magic
from urllib.parse import urlparse

load_dotenv()

class IssueService:
    @staticmethod
    @transaction.atomic
    def update_issues_from_news(keyword):
        today = timezone.now()
        news_items = fetch_news(keyword, today)
        for item in news_items:
            country, sdgs = classify_news(item.get('title', ''), item.get('content', ''))
            if not country.isdigit() or not sdgs.isdigit() or not 1 <= int(country) <= 10 or not 1 <= int(sdgs) <= 17:
                continue
                
            new_issue = Issue.objects.create(
                link=item.get('url', ''),
                writer=item.get('author', ''),
                title=item.get('title', ''),
                content=item.get('content', ''),
                created_at=item.get('publishedAt', '')
            )
            issue_list = IssueList.objects.create(
                issue=new_issue,
                views=0,
                likes=0,
                title=item.get('title', ''),
                description=item.get('description', ''),
                country=country,
                sdgs=sdgs,
                created_at=item.get('publishedAt', '')
            )

            image_url = item.get('urlToImage', '')

            s3_resource = boto3.resource('s3',
                                     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                     region_name=os.getenv('AWS_REGION_NAME'))
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
        
            file_path = f'news_images/{new_issue}'  # S3 내에서 파일을 저장할 경로
            
            # URL이 유효한지 확인하는 함수 추가
            def is_valid_url(url):
                try:
                    result = urlparse(url)
                    return all([result.scheme, result.netloc])
                except Exception:
                    return False

            # URL 유효성 검사 후 처리
            if image_url and is_valid_url(image_url):
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()  # 요청 실패 시 예외 발생

                    image = BytesIO(response.content)
                    mime_type = magic.from_buffer(image.read(2048), mime=True)
                    image.seek(0)  

                    s3_resource.Bucket(bucket_name).put_object(Key=file_path, Body=image, ContentType=mime_type)

                    image_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION_NAME')}.amazonaws.com/{file_path}"
                    new_issue.image_url = image_url
                    new_issue.save()
                    issue_list.image_url = image_url
                    issue_list.save()

                except Exception as e:
                    print(f"Error downloading or uploading image: {e}")
            else:
                print("Invalid or missing image URL.")

    @staticmethod
    @transaction.atomic
    def get_issue_with_increased_view(issue_id):
        IssueList.objects.filter(issue_id=issue_id).update(views=F('views') + 1)
        try:
            return Issue.objects.get(id=issue_id)
        except Issue.DoesNotExist:
            return None
        
    @staticmethod
    def get_recommended_issues():
        recent_time_limit = timezone.now() - timedelta(hours=72)
        return IssueList.objects.annotate(
            ranking=ExpressionWrapper(F('likes') * 10 + F('views'), output_field=fields.IntegerField())
        ).filter(created_at__gte=recent_time_limit).order_by('-ranking')[:3]

    @staticmethod
    def get_issues_by_sdgs(sdgs_number):
        if not 1 <= int(sdgs_number) <= 17:
            return IssueList.objects.none()
        try:
            return IssueList.objects.filter(sdgs=sdgs_number).order_by('-created_at')[:10]
        except (ValueError, TypeError):
            return IssueList.objects.none()

    @staticmethod
    @transaction.atomic
    def toggle_like(user, issue_id):
        issue = Issue.objects.get(id=issue_id)
        issue_list = IssueList.objects.filter(issue=issue)
        issue_like, created = IssueLike.objects.get_or_create(user=user, issue_id=issue_id)
        if not created:
            issue_like.delete()
            issue_list.update(likes=F('likes') - 1)
            return False  # 좋아요 취소
        else:
            issue_list.update(likes=F('likes') + 1)
            return True  # 좋아요 추가
