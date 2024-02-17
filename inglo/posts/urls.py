from django.contrib import admin
from django.urls import path, include
from.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, PostLikeView, FeedbackCreateView, FeedbackDeleteView, FeedbackUpdateView

urlpatterns = [
    path('', PostCreateView.as_view(), name='post-create'),
    path('',PostListView.as_view(), name='post-list'),
    path('<int:post_id>', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>', PostUpdateView.as_view(), name='post-update'),
    path('<int:post_id>', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:post_id>/feedbacks/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('<int:post_id>/feedbacks/<int:feedback_id>', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('<int:post_id>/feedbacks/<int:feedback_id>', FeedbackDeleteView.as_view(), name='feedback-delete'),
]