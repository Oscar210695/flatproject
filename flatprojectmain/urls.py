from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='branches'),
    path('commits/<str:branch>', views.commits, name='commits'),
    path('commit_detail/<str:commit>', views.commit_detail, name='commit_detail'),
    path('merges/', views.list_merges, name='merges'),
    path('add_merge/', views.save_merge, name='add_merge'),
    path('close_merge/<str:id>', views.close_merge, name='close_merge'),
]