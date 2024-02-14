from django.contrib import admin
from django.urls import path, include
from.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, PostLikeView, FeedbackCreateView, FeedbackDeleteView, FeedbackUpdateView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('',PostListView.as_view(), name='post-list'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:post_id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('<int:post_id>/feedbacks/create/', FeedbackCreateView.as_view(), name='feedback-create'),
    path('<int:post_id>/feedbacks/<int:feedback_id>/update/', FeedbackUpdateView.as_view(), name='feedback-update'),
    path('<int:post_id>/feedbacks/<int:feedback_id>/delete/', FeedbackDeleteView.as_view(), name='feedback-delete'),
]