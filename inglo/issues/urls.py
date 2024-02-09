from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueUpdateView, IssueCommentCreate, IssueCommentDetail


urlpatterns = [
    path('api/v1/', include([
        path('issues/recommended/', RecommendedIssueListView.as_view(), name='recommended-issues'),
        path('issues/sdgs/', SDGsIssueListView.as_view(), name='sdgs-issues'),
        path('issues/<int:id>/', IssueDetailView.as_view(), name='issue-detail'),
        path('issues/', IssueUpdateView.as_view(), name='issue-create'),
        path('issues/<int:issue_id>/comments/', IssueCommentCreate.as_view(), name='comment-create'),
        path('issues/<int:issue_id>/comments/<int:pk>/', IssueCommentDetail.as_view(), name='comment-detail'),
    ])),
]