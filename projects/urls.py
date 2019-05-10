from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index , view_project , add_comment , project_search
urlpatterns = [
    path('', index),
    path('<int:id>', view_project),
    path('addcomment', add_comment),
        path('<int:id>', view_project,name="project_details"),
    path('project_search',project_search,name="project_search")
]

