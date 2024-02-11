from django.urls import path, include
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueUpdateView, IssueCommentCreate, IssueCommentUpdate, IssueCommentDelete, IssueLikeView


urlpatterns = [
    path('recommended/', RecommendedIssueListView.as_view(), name='recommended-issues'),
    path('sdgs/', SDGsIssueListView.as_view(), name='sdgs-issues'),
    path('<int:issue_id>/', IssueDetailView.as_view(), name='issue-detail'),
    path('', IssueUpdateView.as_view(), name='issue-create'),
    path('<int:issue_id>/comments/', IssueCommentCreate.as_view(), name='comment-create'),
    path('<int:issue_id>/comments/<int:comment_id>/update/', IssueCommentUpdate.as_view(), name='comment-update'),
    path('<int:issue_id>/comments/<int:comment_id>/delete/', IssueCommentDelete.as_view(), name='comment-delete'),
    path('<int:issue_id>/like/', IssueLikeView.as_view(), name='issue-like'),
]