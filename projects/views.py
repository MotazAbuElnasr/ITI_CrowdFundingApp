from django.http import HttpResponse
import datetime
from django.shortcuts import render
from .models import Comment, Project , ProjectImage , Donation
from django.db.models import Avg,Sum
from django import template
from django.contrib.auth.models import User

register = template.Library()

def index() :
    pass 

def view_project(request,id): 
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
        "imgs":imgs,
        "users_info":users_info,
        "avg_rate":range(int(avg_rate['rate__avg'])),
        "rest_of_stars":range((5-int(avg_rate['rate__avg'])))
    }
    return render(request, 'projects/project_page.html', context)
