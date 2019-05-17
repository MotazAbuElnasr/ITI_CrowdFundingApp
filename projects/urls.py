from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index, project_search,myProjects,myDonations,create_project,project_images,list_projects_with_categories
urlpatterns = [
    path('', index),
    path('project_search', project_search, name="project_search"),
    path('<int:id>/', include('single_project.urls')),
    path('myProjects', myProjects, name="myProjects"),
    path('myDonations', myDonations, name="myDonations"),
    path('add_project',create_project , name="create_project"),
    path('project_images/<int:project_id>/',project_images , name="project_images"),
    path('app',list_projects_with_categories ),



]
