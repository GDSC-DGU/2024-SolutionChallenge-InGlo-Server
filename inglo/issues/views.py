from django.utils import timezone
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now
from datetime import timedelta
from rest_framework import generics
from rest_framework.response import Response
from .models import Issue, IssueList, IssueComment
from .serializers import IssueSerializer, IssueListSerializer, IssueCommentSerializer
from rest_framework import status
from .services import update_issues_from_news

class RecommendedIssueListView(generics.ListAPIView):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        """
        좋아요 수와 조회수를 기반으로 랭킹을 매긴 후,
        가장 높은 랭킹의 이슈 3개를 반환.
        좋아요 하나 = 조회수 10개로 계산하여 랭킹 매김.
        단, 생성된지 72시간 이내의 글에 대해서만.
        """
        recent_time_limit = Now() - timedelta(hours=72)
        queryset = IssueList.objects.annotate(
            ranking=ExpressionWrapper(F('likes')*10 + F('views'), output_field=fields.IntegerField())
        ).filter(created_at__gte=recent_time_limit).order_by('-ranking')[:3]
        return queryset

class SDGsIssueListView(generics.ListAPIView):
    serializer_class = IssueListSerializer

    def get_queryset(self):
        """
        클라이언트로부터 받은 SDGs 헤더 값을 기반으로
        해당 SDGs 카테고리와 관련된 최신 10개의 이슈를 반환.
        """
        sdgs_number = self.request.headers.get('SDGs')
        
        # SDGs 헤더 값 유효성 검사. 비어있거나, 1~17 사이의 정수가 아니면 빈 쿼리셋 반환
        if sdgs_number is None or not sdgs_number.isdigit() or not 1 <= int(sdgs_number) <= 17:
            return IssueList.objects.none()
        
        try:
            sdgs_number = int(sdgs_number)
            return IssueList.objects.filter(sdgs=sdgs_number).order_by('-created_at')[:10]
        except (ValueError, TypeError):
            return IssueList.objects.none()  # 유효하지 않은 경우, 빈 쿼리셋 반환

class IssueDetailView(generics.RetrieveAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = 'id'

class IssueUpdateView(generics.APIView):
    """
    외부 News API로부터 데이터를 가져와
    분류모델을 돌려서
    Issue, IssueImage, IssueList에 저장
    """

    def post(self, request, *args, **kwargs):
        news_properties = update_issues_from_news(keyword='SDGs', today=timezone.now())

        for item in news_properties:
            # Issue 추가
            issue_serializer = IssueSerializer(data={
                "link": item['link'],
                "writer": item['writer'],
                "title": item['title'],
                "content": item['content'],
                "image_url": item['image_url'], 
                "created_at": item['created_at'],
            })
            if issue_serializer.is_valid():
                issue = issue_serializer.save()

                # IssueList 추가
                issue_list_serializer = IssueListSerializer(data={
                    "issue": issue.id,
                    "views": 0,
                    "likes": 0,
                    "title": item['title'],
                    "description": item['description'],
                    "country": item['country'],
                    "sdgs": item['sdgs'],
                    "created_at": item['created_at'],
                })
                if issue_list_serializer.is_valid():
                    issue_list_serializer.save()
        
        return Response({"message": "Issues successfully updated."}, status=status.HTTP_200_OK)
