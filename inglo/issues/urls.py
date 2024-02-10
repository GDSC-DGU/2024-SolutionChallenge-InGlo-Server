from django.urls import path, include
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueUpdateView, IssueCommentCreate, IssueCommentUpdate, IssueCommentDelete, IssueLikeView


urlpatterns = [
    path('api/v1/', include([
        path('issues/recommended/', RecommendedIssueListView.as_view(), name='recommended-issues'),
        path('issues/sdgs/', SDGsIssueListView.as_view(), name='sdgs-issues'),
        path('issues/<int:id>/', IssueDetailView.as_view(), name='issue-detail'),
        path('issues/', IssueUpdateView.as_view(), name='issue-create'),
        path('issues/<int:issue_id>/comments/', IssueCommentCreate.as_view(), name='comment-create'),
        path('issues/<int:issue_id>/comments/<int:pk>/update/', IssueCommentUpdate.as_view(), name='comment-update'),
        path('issues/<int:issue_id>/comments/<int:pk>/delete/', IssueCommentDelete.as_view(), name='comment-delete'),
        path('issues/<int:issue_id>/like/', IssueLikeView.as_view(), name='issue-like'),
    ])),
]