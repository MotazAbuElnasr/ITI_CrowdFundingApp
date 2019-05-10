from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import index , view_project , add_comment
from .views import view_project
urlpatterns = [
    path('', index),
    path('<int:id>', view_project),
    path('addcomment', add_comment),
]
