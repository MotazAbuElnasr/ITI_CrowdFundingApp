from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index, project_search,myProjects,myDonations
urlpatterns = [
    path('', index),
    path('project_search', project_search, name="project_search"),
    path('<int:id>/', include('single_project.urls')),
    path('myProjects', myProjects, name="myProjects"),
    path('myDonations', myDonations, name="myDonations"),


]
