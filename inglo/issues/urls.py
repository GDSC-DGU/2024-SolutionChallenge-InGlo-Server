from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueUpdateView, IssueCommentViewSet

router = DefaultRouter()
router.register(r'issues/comments', IssueCommentViewSet)

urlpatterns = [
    path('api/v1/', include([
        path('', include(router.urls)),
        path('issues/recommended/', RecommendedIssueListView.as_view(), name='recommended-issues'),
        path('issues/sdgs/', SDGsIssueListView.as_view(), name='sdgs-issues'),
        path('issues/<int:id>/', IssueDetailView.as_view(), name='issue-detail'),
        path('issues/', IssueUpdateView.as_view(), name='issue-create'),
    ])),
]