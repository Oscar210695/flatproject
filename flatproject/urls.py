from django.contrib import admin
from django.urls import path, include
from flatprojectapi import views
from rest_framework import routers

router = routers.DefaultRouter() 
router.register(r'merges', views.getMerges, 'flatprojectMerges')  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('flatprojectapi.urls')),
    path('api/', include(router.urls)),
    path('', include('flatprojectmain.urls')),
]
