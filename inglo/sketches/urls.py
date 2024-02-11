from django.urls import path, include
from .views import ProblemListView, ProblemCreateView, HMWListView, HMWCreateView


urlpatterns = [
    path('<int:sdgs>/problem/', ProblemListView.as_view(), name='problem-list'),
    path('<int:sdgs>/problem/create/', ProblemCreateView.as_view(), name='problem-create'),
    path('<int:problem_id>/hmw/', HMWListView.as_view(), name='hmw-list'),
    path('<int:problem_id>/hmw/create/', HMWCreateView.as_view(), name='hmw-create'),
    # path('<int:problem_id>/crazy8/', Crazy8ListView.as_view(), name='crazy8-list'),
    # path('<int:problem_id>/crazy8/create/', Crazy8CreateView.as_view(), name='crazy8-create'),
    # path('<int:problem_id>/crazy8/vote/', Crazy8VoteView.as_view(), name='crazy8-vote'),
]