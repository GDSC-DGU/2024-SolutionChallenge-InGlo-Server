from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueListViewSet, IssueViewSet, IssueCommentViewSet, RecommendedIssueListView, SDGsIssueListView

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('recommended-issues/', RecommendedIssueListView.as_view(), name='recommended-issues'),
    path('sdgs-issues/', SDGsIssueListView.as_view(), name='sdgs-issues'),
]