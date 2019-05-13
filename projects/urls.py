from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index, project_search
urlpatterns = [
    path('', index),
    path('project_search', project_search, name="project_search"),
    path('<int:id>/', include('single_project.urls')),

]
