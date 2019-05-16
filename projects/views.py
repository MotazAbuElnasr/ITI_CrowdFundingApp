from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
import math
from django import template
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q, Sum
from django.db.models.query import prefetch_related_objects
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Donation, Project, ProjectImage, Category 
from .forms import ProjectForm, ProjectImageForm

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
        details__icontains="project")).distinct().annotate

def myProjects(request):
    current_user = request.user.id

    myProjects = Project.objectsfilter(user_id=current_user).order_by('start_date')
# preparing User Projects in One List
    myProjectsList = []
    for project in myProjects:
        print ("my projects : ",myProjectsList)
        myProjectsList.append({
                'id': project.id,
                'title': project.title,
                'details': project.details,
                'target': project.target,
                'start_date': project.start_date,
                'img': (project.projectimage_set.first().img.url if ( project.projectimage_set.count() > 0 ) else "/media/project_images/NotFound.png")
    })    
    return render(request, 'projects/myprojects.html', {'myProjects': myProjectsList})
      
def myDonations(request):
    current_user = request.user.id

    myDonations = Project.objectsfilter(user_id=current_user).order_by('start_date')
# preparing User Donations in One List
   
    myDonationsList = []
    for Donation in myDonationsList:
        
        myDonationsList.append({
            'id': Donation.id,
            'amount': project.title,
            
    })    
    return render(request, 'projects/myDonations.html', {'myDonations': myDonationList})

# create new project function
@login_required
def create_project(request):
    if request.method == 'GET' :
        form = ProjectForm()
    else:
        form = ProjectForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            project_id =Project.objects.latest('id').id
            return HttpResponseRedirect(reverse('/projects/project_images/', args=(project_id,)))


    return render(request,'projects/add.html', {'form': form})
def project_images(request, project_id):
    if request.method == 'GET' :
        form = ProjectImageForm()
    else:
        form = ProjectImageForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            for f in files:
                ProjectForm.objects.create(project_id=project_id,img=f)
           
            return redirect('/projects')
    return render(request,'projects/upload_images.html', {'form': form})


