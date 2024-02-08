from django.utils import timezone
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now
from datetime import timedelta
from rest_framework import generics, viewsets
from rest_framework.response import Response
from .models import Issue, IssueList, IssueComment
from .serializers import IssueSerializer, IssueListSerializer, IssueCommentSerializer

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
