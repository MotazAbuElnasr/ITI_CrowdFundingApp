from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Project(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    details = models.TextField()
    body = models.CharField(max_length=400)

class Images(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
       return project.title