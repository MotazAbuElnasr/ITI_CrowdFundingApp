from django.contrib import admin
from .models import Project,ProjectImage, Category, Comment

# Register your models here.
admin.site.register(Project)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(ProjectImage)
