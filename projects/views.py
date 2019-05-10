import datetime
from django.http import HttpResponse
import datetime
from django.shortcuts import render
from .models import Comment, Project , ProjectImage , Donation
from django.db.models import Avg,Sum, Count ,Q
from django import template
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Comment, Donation, Project, ProjectImage

register = template.Library()

def index(request):
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
            'target':project.target,
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

def view_project(request,id,comment=''): 
    project = Project.objects.get(id=id)
    featured_img = project.projectimage_set.first().img.url
    comments = list(project.comment_set.values())
    imgs = project.projectimage_set.all()
    # get user name by populating comments
    populated_comments = project.comment_set.all()
    user_names = [(obj.user.username , obj.user.id ) for obj in populated_comments]
    # get donation amount
    users_info=[]
    for i,user in enumerate(user_names):
        amount = Donation.objects.filter(user_id=user[1],project_id=id).aggregate(Sum('amount'))
        if amount['amount__sum'] == None:
            amount['amount__sum']="0"
        user_info = {
            "user_name":user_names[i][0],
            "amount":int(amount['amount__sum']) 
            }
        users_info.append(dict(user_info))

    avg_rate = Comment.objects.filter(project_id = id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"
    # to get specific index for example we use list(prokect.projectimage_set.values())[2]
    # to get comments using reverse query we use list(project.comment_set.values())
    context = {
        "project":project,
        "featured_img":featured_img,
        "comments":comments,
        "comment":comment,
        "imgs":imgs,
        "users_info":users_info,
        "avg_rate":range(int(avg_rate['rate__avg'])),
        "rest_of_stars":range((5-int(avg_rate['rate__avg'])))
    }
    return render(request, 'projects/project_page.html/', context)
def add_comment(request):
    project_id= request.POST.get('project_id')
    comment= request.POST.get('comment')
    rating= request.POST.get('rating')
    if not comment :
        messages.error(request,"The comment is required")
    if not rating : 
        messages.warning(request,"The rating is required")
    messages.info(request,comment)
    return redirect('/projects/'+str(project_id))


def project_search(request):
    query = request.GET.get('q')
    result = []
    # get the query result 
    if query:
        result = Project.objects.filter(
            Q(title__icontains=query)|
            Q(title__icontains=query)
        ).distinct().annotate(comment_rate=Avg('comment__rate'))
    resultList =[]

    # preparing the result to the tempalte
    for project in result:
        resultList.append({
            'id':project.id,
            'title':project.title,
            'rate':project.comment_rate,
            'target':project.target,
            'img':project.projectimage_set.first().img.url
            })
    return render(request, 'projects/search_result.html',{'result':result})
    Project.objects.filter(Q(title__icontains="project")|Q(details__icontains="project")).distinct().annotate(comment_rate=Avg('comment__rate'))
