import datetime

from django import template
from django.contrib.auth.models import User
from django.db.models import Avg, Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Comment, Donation, Project, ProjectImage

register = template.Library()

def index() :
    pass 

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
        user_info = {"user_name":user_names[i][0],"amount":int(amount['amount__sum'])}
        users_info.append(dict(user_info))

    avg_rate = Comment.objects.filter(project_id = id).aggregate(Avg('rate'))
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