from django.urls import path, include
from .views import Crazy8VoteView, SketchUpdateView
from rest_framework.routers import SimpleRouter
from .views import ProblemViewSet, HMWViewSet, Crazy8ViewSet, SketchViewSet, SketchDetailViewSet

router = SimpleRouter()

urlpatterns = [
    path('<int:sdgs>/problem/', ProblemViewSet.as_view({'get': 'list', 'post': 'create'}), name='problem-list-create'),
    path('<int:problem_id>/hmw/', HMWViewSet.as_view({'get': 'list', 'post': 'create','patch':'update'}), name='hmw-list-create'),
    path('<int:problem_id>/crazy8/', Crazy8ViewSet.as_view({'get': 'list', 'post': 'create'}), name='crazy8-list'),
    path('', SketchViewSet.as_view({'get': 'list', 'post': 'create'}), name='sketch-list-create'),
    path('detail/<int:sketch_id>', SketchDetailViewSet.as_view({'get':'retrieve', 'delete':'destroy'}), name='sketch-detail-delete'),
    path('<int:problem_id>', SketchUpdateView.as_view(), name='sketch-update'),
    path('<int:problem_id>/crazy8/vote/', Crazy8VoteView.as_view(), name='crazy8-vote'),
]