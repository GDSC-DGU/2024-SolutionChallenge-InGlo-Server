from django.utils import timezone
from django.db.models import F, ExpressionWrapper, fields
from django.db.models.functions import Now
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from datetime import timedelta
from rest_framework import generics, status, views
from rest_framework.response import Response
from .models import Issue, IssueList, IssueComment, IssueLike
from .serializers import IssueSerializer, IssueListSerializer, IssueCommentSerializer
from .services.news_updater import update_issues_from_news
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated

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

class IssueDetailView(views.APIView):

    def get(self, request, id):
        """
        이슈 리스트에서 특정 이슈를 클릭하면,
        해당 이슈의 조회수를 1 증가시키고 상세 정보를 반환.
        """
        IssueList.objects.filter(pk=id).update(views=F('views') + 1)
        issue = Issue.objects.get(pk=id)
        serializer = IssueSerializer(issue, context={'request': request})
        return Response(serializer.data)

class IssueUpdateView(views.APIView):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        외부 News API로부터 데이터를 가져와
        분류모델을 돌려서
        Issue, IssueImage, IssueList에 저장
        """
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
    
class IssueCommentCreate(views.APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request, issue_id):
        """
        현재 들어와있는 이슈에 대한 댓글을 추가
        """
        user=request.user
        issue = get_object_or_404(Issue, pk=issue_id)
        try:
            parent_comment_id = request.data.get('parent_comment')
            parent_comment_id = None if not parent_comment_id else int(parent_comment_id)
        except ValueError:
            raise ValidationError({'parent_comment': ['Invalid parent comment ID.']})

        serializer = IssueCommentSerializer(data={
            "parent_comment": parent_comment_id,
            "content": request.data.get('content'),
            "created_at": timezone.now(),
        })
        if serializer.is_valid():
            serializer.save(user=user, issue=issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class IssueCommentDetail(views.APIView):

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_object(self, pk):
        """
        선택한 댓글에 대한 수정, 삭제
        """
        try:
            return IssueComment.objects.get(pk=pk)
        except IssueComment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, issue_id, pk):
        comment = self.get_object(pk)
        serializer = IssueCommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, issue_id, pk):
        comment = self.get_object(pk)
        if comment.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueLikeView(views.APIView):

    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request, issue_id):
        """
        특정 이슈에 대한 좋아요를 추가
        """
        # 사용자가 이미 좋아요를 눌렀는지 확인
        like_exists = IssueLike.objects.filter(user=request.user, issue_id=issue_id).exists()

        if like_exists:
            return Response({"message": "You have already liked this issue."}, status=status.HTTP_400_BAD_REQUEST)

        IssueLike.objects.create(user=request.user, issue_id=issue_id)
        issue_list = get_object_or_404(IssueList, issue_id=issue_id)
        issue_list.likes += 1
        issue_list.save()
        return Response({"message": "Like added successfully."}, status=status.HTTP_201_CREATED)
    
    @transaction.atomic
    def delete(self, request, issue_id):
        """
        특정 이슈에 대한 좋아요를 삭제
        """
        # IssueLike 레코드 삭제
        like = get_object_or_404(IssueLike, user=request.user, issue_id=issue_id)
        like.delete()
        # IssueList의 좋아요 수 업데이트
        issue_list = get_object_or_404(IssueList, issue_id=issue_id)
        issue_list.likes -= 1
        issue_list.save()
        return Response({"message": "Like removed successfully."}, status=status.HTTP_204_NO_CONTENT)