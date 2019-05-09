from django.shortcuts import render
from django.http import HttpResponse
from projects.models import Project
from django.db.models import Avg, Count
# Create your views here.

def homepage(request):
    topRatedProjects = Project.objects.annotate(comment_rate=Avg('comment__rate')).order_by('-comment_rate')[:5]
    latestProjects = Project.objects.order_by('start_date')[:5]
    featuredProjects = Project.objects.filter(featured=True).order_by('start_date')[:5]

    #preparing Top Rated Projects in One List 
    topRatedProjectsList =[]
    for project in topRatedProjects:
        topRatedProjectsList.append({
            'id':project.id,
            'title':project.title,
            'rate':project.comment_rate,
            'img':project.projectimage_set.first().img.url
            })


    #preparing Latest Projects in One List 
    latestProjectsList =[]
    for project in latestProjects:
        latestProjectsList.append({
            'id':project.id,
            'title':project.title,
            'details':"asdfdsaf12",
            'target':project.target,
            'start_date':project.start_date,
            'img':project.projectimage_set.first().img.url
            })
    
    #preparing Featured Projects in One List 
    featuredProjectsList =[]
    for project in featuredProjects:
        featuredProjectsList.append({
            'id':project.id,
            'title':project.title,
            'details':"asdfdsaf12",
            'target':project.target,
            'start_date':project.start_date,
            'img':project.projectimage_set.first().img.url
            })
    # imgSrc = topRatedProjects[0].projectimage_set.first().img.url
    context= {
        'topRatedProjectsList':topRatedProjectsList,
        'latestProjectsList':latestProjectsList,
        'featuredProjectsList':featuredProjectsList,
         }
    return render(request,"projects/index.html",context)
