from django.contrib import admin
from django.urls import path, include
from.views import PostCreateView, PostListView, PostDetailView, PostUpdateView, PostDeleteView, PostLikeView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('/',PostListView.as_view(), name='post-list'),
    path('<int:post_id>/', PostDetailView.as_view(), name='post-detail'),
    path('<int:post_id>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:post_id>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
]