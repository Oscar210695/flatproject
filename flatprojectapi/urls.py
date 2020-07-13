from django.urls import path
from .views import BranchView, CommitView, CommitDetailView, MergeBranchesView

urlpatterns = [
    path('branches/', BranchView.as_view()),
    path('commits/<str:branch>', CommitView.as_view()),
    path('commit_detail/<str:commit>', CommitDetailView.as_view()),
    path('merge_branch/', MergeBranchesView.as_view()),
]