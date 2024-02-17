from django.contrib import admin
from django.urls import path, include
from.views import PostViewSet, PostDetailViewSet, PostLikeView, FeedbackCreateView, FeedbackUpdateDeleteViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()

urlpatterns = [
    path('', PostViewSet.as_view({'get':'list','post':'create'}), name='post-create-list'),
    path('<int:post_id>', PostDetailViewSet.as_view({'get':'retrieve','patch':'update','delete':'destroy'}), name='post-detail-update-delete'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:post_id>/feedbacks/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('<int:post_id>/feedbacks/<int:feedback_id>', FeedbackUpdateDeleteViewSet.as_view({'patch':'update','delete':'destroy'}), name='post-detail-update-delete'),
]