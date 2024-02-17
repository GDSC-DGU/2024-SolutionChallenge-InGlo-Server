from django.urls import path, include
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueCreateView, IssueCommentCreate, IssueCommentUpdateDeleteViewSet, IssueLikeView
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('recommended/', RecommendedIssueListView.as_view(), name='recommended-issues'),
    path('sdgs/<int:sdgs>', SDGsIssueListView.as_view(), name='sdgs-issues'),
    path('<int:issue_id>', IssueDetailView.as_view(), name='issue-detail'),
    path('', IssueCreateView.as_view(), name='issue-create'),
    path('<int:issue_id>/comments/', IssueCommentCreate.as_view(), name='comment-create'),
    path('<int:issue_id>/comments/<int:comment_id>', IssueCommentUpdateDeleteViewSet.as_view({'patch':'update','delete':'destroy'}), name='comment-update-delete'),
    path('<int:issue_id>/like/', IssueLikeView.as_view(), name='issue-like'),
]