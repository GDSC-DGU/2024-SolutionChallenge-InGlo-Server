from django.db.models import F
from django.db import transaction
from django.db.models import ExpressionWrapper, fields
from django.utils import timezone
from ..models import Issue, IssueList, IssueLike
from datetime import timedelta
from ..utils.classifier import classify_news
from ..utils.news_api import fetch_news

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
                image_url=item.get('urlToImage', ''),
                created_at=item.get('publishedAt', '')
            )
            IssueList.objects.create(
                issue=new_issue,
                views=0,
                likes=0,
                title=item.get('title', ''),
                description=item.get('description', ''),
                country=country,
                sdgs=sdgs,
                created_at=item.get('publishedAt', '')
            )

    @staticmethod
    @transaction.atomic
    def get_issue_with_increased_view(issue_id):
        IssueList.objects.filter(issue__id=issue_id).update(views=F('views') + 1)
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
        if not sdgs_number.isdigit() or not 1 <= int(sdgs_number) <= 17:
            return IssueList.objects.none()
        try:
            sdgs_number = int(sdgs_number)
            return IssueList.objects.filter(sdgs=sdgs_number).order_by('-created_at')[:10]
        except (ValueError, TypeError):
            return IssueList.objects.none()

    @staticmethod
    @transaction.atomic
    def toggle_like(user, issue_id):
        issue_like, created = IssueLike.objects.get_or_create(user=user, issue_id=issue_id)
        if not created:
            issue_like.delete()
            return False  # 좋아요 취소
        else:
            return True  # 좋아요 추가
