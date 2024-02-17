from django.urls import path, include
from .views import ProblemListView, ProblemCreateView, ProblemChooseView, HMWListView, HMWCreateView, Crazy8ListView, Crazy8CreateView, Crazy8VoteView, SketchListView, SketchUpdateView, SketchDetailView, SketchDeleteView


urlpatterns = [
    path('<int:sdgs>/problem/', ProblemListView.as_view(), name='problem-list'),
    path('<int:sdgs>/problem/', ProblemCreateView.as_view(), name='problem-create'),
    path('<int:problem_id>/hmw/', HMWListView.as_view(), name='hmw-list'),
    path('<int:problem_id>/hmw/', HMWCreateView.as_view(), name='hmw-create'),
    path('<int:problem_id>/crazy8/', Crazy8ListView.as_view(), name='crazy8-list'),
    path('<int:problem_id>/crazy8/', Crazy8CreateView.as_view(), name='crazy8-create'),
    path('<int:problem_id>/crazy8/vote/', Crazy8VoteView.as_view(), name='crazy8-vote'),
    path('', ProblemChooseView.as_view(), name='problem-choose'),
    path('', SketchListView.as_view(), name='sketch-list'),
    path('<int:problem_id>', SketchUpdateView.as_view(), name='sketch-update'),
    path('<int:sketch_id>', SketchDetailView.as_view(), name='sketch-detail'),
    path('<int:sketch_id>', SketchDeleteView.as_view(), name='sketch-delete'),
]