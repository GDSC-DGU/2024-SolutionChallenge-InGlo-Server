from django.db.models import F
from django.db import transaction
from django.db.models import ExpressionWrapper, fields
from django.utils import timezone
from ..models import Issue, IssueList, IssueLike
from datetime import timedelta
from ..utils.classifier import classify_news
from ..utils.news_api import fetch_news
from dotenv import load_dotenv
from dateutil.parser import parse as parse_datetime
from datetime import datetime
from io import BytesIO
import logging
import os
import magic
from urllib.parse import urlparse
import aioboto3
import aiohttp
import asyncio
from asgiref.sync import sync_to_async

logger = logging.getLogger('django')
load_dotenv()

class IssueService:

    @staticmethod
    async def is_valid_url(url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            logger.error(logging.ERROR, f"Error checking if {url} is a valid URL")
            return False
    @staticmethod
    async def provide_none():
        return None
        
    @staticmethod
    async def download_and_upload_image(session, image_url, file_path):
        try:
            async with session.get(image_url) as response:
                response.raise_for_status()
                content = await response.read()
                image = BytesIO(content)
                mime_type = magic.from_buffer(image.read(2048), mime=True)
                image.seek(0)
                bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')
                region_name = os.getenv('AWS_REGION_NAME')
                session = aioboto3.Session()
                async with session.client('s3', region_name=os.getenv('AWS_REGION_NAME'),
                                          aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                          aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')) as s3:
                    await s3.upload_fileobj(image, os.getenv('AWS_STORAGE_BUCKET_NAME'), file_path, ExtraArgs={"ContentType": mime_type})

                return f"https://{bucket_name}.s3.{region_name}.amazonaws.com/{file_path}"
        except Exception as e:
            logger.error(logging.ERROR,f"Error downloading or uploading image: {e}")
            return None

    @staticmethod
    async def update_issues_from_news_async(news_items):

        tasks = []
        
        async with aiohttp.ClientSession() as session:

            insert_list = []

            for item in news_items:
                if await sync_to_async(Issue.objects.filter(content=item.get('content')).exists)():
                    continue
                insert_list.append(item)
                image_url = item.get('image_url', '')
                file_path = f"news_images/{item.get('article_id','')}"

                if image_url and await IssueService.is_valid_url(image_url):
                    task = IssueService.download_and_upload_image(session, image_url, file_path)  # await 추가
                    tasks.append(task)
                else:
                    tasks.append(IssueService.provide_none())


            images = await asyncio.gather(*tasks,return_exceptions=True)  # 각 작업의 결과를 기다립니다.
            await sync_to_async(IssueService.save_issues_and_images, thread_sensitive=True)(insert_list, images)

    @staticmethod
    def save_issues_and_images(insert_list, images):
        for item, image_url in zip(insert_list, images):
            if item.get('content') is None: #본문이 비어있으면 for문의 다음 item으로 넘어감
                    continue
            
            sdgs = classify_news(item.get('content', ''))

            if not sdgs.isdigit() or not 1 <= int(sdgs) <= 17: #분류모델 돌린 결과 나온 sdgs가 1~17 사이의 숫자가 아니면 for문의 다음 item으로 넘어감
                continue

            pub_date = item.get('pubDate', '')
            created_at = parse_datetime(pub_date) if parse_datetime(pub_date) is not None else datetime.now()
            new_issue = Issue.objects.create(
                link=item.get('link', ''),
                writer=item.get('creator', ''),
                title=item.get('title', ''),
                content=item.get('content', ''),
                image_url=image_url,
                created_at=created_at
            )
            issue_list = IssueList.objects.create(
                issue=new_issue,
                views=0,
                likes=0,
                title=item.get('title', ''),
                description=item.get('description', ''),
                country=item.get('country', ''),
                sdgs=sdgs,
                image_url=image_url,
                created_at=created_at
            )

    @staticmethod
    def update_issues_from_news(keyword):
        news_items = fetch_news(keyword)
        asyncio.run(IssueService.update_issues_from_news_async(news_items))

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
