from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import datetime
import math
from django import template
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Sum
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Donation, Project, ProjectImage

register = template.Library()

@login_required
def index(request):
    topRatedProjects = Project.objects.annotate(
        comment_rate=Avg('comment__rate')).order_by('-comment_rate')[:5]
    latestProjects = Project.objects.order_by('start_date')[:5]
    featuredProjects = Project.objects.filter(
        featured=True).order_by('start_date')[:5]

    # preparing Top Rated Projects in One List
    topRatedProjectsList = []
    for project in topRatedProjects:
        topRatedProjectsList.append({
            'id': project.id,
            'title': project.title,
            'rate': project.comment_rate,
            'target': project.target,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })

    # preparing Latest Projects in One List
    latestProjectsList = []
    for project in latestProjects:
      
        latestProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': project.details,
            'target': project.target,
            'start_date': project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })

    # preparing Featured Projects in One List
    featuredProjectsList = []
    for project in featuredProjects:
    
        featuredProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': project.details,
            'target': project.target,
            'start_date': project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
            
        })
    # imgSrc = topRatedProjects[0].projectimage_set.first().img.url
    context = {
        'topRatedProjectsList': topRatedProjectsList,
        'latestProjectsList': latestProjectsList,
        'featuredProjectsList': featuredProjectsList,
    }
    return render(request, "projects/index.html", context)

@login_required
def project_search(request):
    query = request.GET.get('q')
    result = []
    # get the query result
    if query:
        result = Project.objects.filter(
            Q(title__icontains=query) |
            Q(title__icontains=query)
        ).distinct().annotate(comment_rate=Avg('comment__rate'))
    resultList = []

    # preparing the result to the tempalte
    for project in result:
        print(project)
        resultList.append({
            'id':project.id,
            'title': project.title,
            'rate': project.comment_rate,
            'target': project.target,
            'details': project.details,
            'start_date':project.start_date,
            'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
        })
    return render(request, 'projects/search_result.html', {'result': resultList})

    Project.objects.filter(Q(title__icontains="project") | Q(
        details__icontains="project")).distinct().annotate()
