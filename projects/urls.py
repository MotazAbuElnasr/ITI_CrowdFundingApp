from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index, view_project, project_search

urlpatterns = [
    path('<int:id>', view_project, name="project_details"),
    path('project_search', project_search, name="project_search")
    # path('', index),
]
