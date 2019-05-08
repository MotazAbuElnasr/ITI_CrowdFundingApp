from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
import uuid
import os
class Category(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField( upload_to="categories/")


class Project(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    details = models.TextField()
    body = models.CharField(max_length=400)

# function to generate unique name for uploaded imgs
def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('projects/', filename)
class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    img = models.ImageField( upload_to=get_file_path)
    def __str__(self):
       return self.project.title
