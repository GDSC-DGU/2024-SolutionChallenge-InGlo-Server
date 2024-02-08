from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecommendedIssueListView, SDGsIssueListView, IssueDetailView, IssueUpdateView

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('recommended-issues/', RecommendedIssueListView.as_view(), name='recommended-issues'),
    path('sdgs-issues/', SDGsIssueListView.as_view(), name='sdgs-issues'),
    path('issues/<int:id>/', IssueDetailView.as_view(), name='issue-detail'),
    path('update-issues/', IssueUpdateView.as_view(), name='issue-update'),
]