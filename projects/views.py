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

from .forms import AddCommentForm
from .models import Comment, Donation, Project, ProjectImage

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
            'img': project.projectimage_set.first().img.url
        })

    # preparing Latest Projects in One List
    latestProjectsList = []
    for project in latestProjects:
        latestProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': "asdfdsaf12",
            'target': project.target,
            'start_date': project.start_date,
            'img': project.projectimage_set.first().img.url
        })

    # preparing Featured Projects in One List
    featuredProjectsList = []
    for project in featuredProjects:
        featuredProjectsList.append({
            'id': project.id,
            'title': project.title,
            'details': "asdfdsaf12",
            'target': project.target,
            'start_date': project.start_date,
            'img': project.projectimage_set.first().img.url
        })
    # imgSrc = topRatedProjects[0].projectimage_set.first().img.url
    context = {
        'topRatedProjectsList': topRatedProjectsList,
        'latestProjectsList': latestProjectsList,
        'featuredProjectsList': featuredProjectsList,
    }
    return render(request, "projects/index.html", context)

def get_users_info (project_id,comments,user_names) :
    if len(user_names) == 0 :
        return []
    users_info=[]
    for i, user in enumerate(user_names):
        amount = Donation.objects.filter(user_id=user[1], project_id=project_id).aggregate(Sum('amount'))
    if amount['amount__sum'] == None:
        amount['amount__sum'] = "0"
    user_info = {
        "user_name": user_names[i][0],
        "amount": int(amount['amount__sum']),
        "comment": comments[i]['comment'],
        "rate": comments[i]['rate']
    }
    users_info.append(dict(user_info))
    return users_info

def get_donators_info(p_id):
    # get donation info
    all_donations = Donation.objects.filter(
        project_id=p_id).prefetch_related('user')
    donation_info = list(all_donations.values('user_id').annotate(sum=Sum('amount')).order_by('-sum'))
    donators = []
    donator_id = []
    for entry in donation_info:
        for data in all_donations:
            if data.user.id == entry['user_id'] and data.user.id not in donator_id:
                donators.append(
                    {"user_name": data.user.username, "sum": entry['sum']})
                # to make sure that the name won't be repeated
                donator_id.append(data.user.id)
    return donators

@login_required
def view_project(request, id):
    current_user = request.user.id
    project = Project.objects.get(id=id)
    featured_img = project.projectimage_set.first().img.url
    comments = list(project.comment_set.values())
    imgs = project.projectimage_set.all()
    # get user name by populating comments
    populated_comments = project.comment_set.all()
    user_names = [(entry.user.username, entry.user.id)
                  for entry in populated_comments]

        # check if the user can comment
    user_comments_count = populated_comments.filter(
        user_id=current_user, project_id=id).count()
    can_comment = not bool(user_comments_count)

    avg_rate = Comment.objects.filter(project_id=id).aggregate(Avg('rate'))
    if avg_rate['rate__avg'] == None:
        avg_rate['rate__avg'] = "0"
    # Get the progress of project
    total_amount = Donation.objects.filter(
        project_id=id).aggregate(Sum('amount'))['amount__sum']
    target = project.target
    if not total_amount:
        total_amount = 0
    percentage = math.floor(total_amount*100/target)
    can_cancel = True if percentage < 25 and project.user_id == current_user else False
    can_report = True if project.user_id != current_user else False
    # ِAdd comment form
    form = AddCommentForm()
    # get donation amount for everyh person
    users_info = get_users_info(id,comments, user_names)
    donators = get_donators_info(id)
    context = {
        "project": project,
        "featured_img": featured_img,
        "form": form,
        "imgs": imgs,
        'comments': comments,
        "donators": donators,
        "users_info": users_info,
        "avg_rate": range(int(avg_rate['rate__avg'])),
        "rest_of_stars": range((5-int(avg_rate['rate__avg']))),
        "total_amount": total_amount,
        "target": target,
        "percentage": percentage,
        "can_comment": can_comment,
        "can_cancel" : can_cancel,
        "can_report" : can_report,
    }
    return render(request, 'projects/project_page.html/', context)
@login_required
def add_comment(request):
    current_user = request.user.id
    form = AddCommentForm(request.POST)
    if form.is_valid():
        comment = Comment()
        comment.rate = int(form['rate'].value())
        comment.comment = form['comment'].value()
        comment.project_id = int(request.POST['project_id'])
        comment.user_id = current_user
        comment.save()
        return redirect('/projects/'+str(comment.project_id))
    return redirect('/projects/'+str(comment.project_id))
@login_required
def donate(request):
    current_user = request.user.id
    donation = Donation()
    donation.amount = request.POST['amount']
    donation.project_id = request.POST['project_id']
    donation.user_id = current_user
    donation.save()
    return redirect('/projects/'+str(donation.project_id))

def cancel_project(request):
    current_user = request.user.id
    p_id = request.POST['project_id']
    project = Project.objects.get(id=p_id)
    # check if the deleter is the project owner
    if current_user == project.user_id:
        project.delete()
        return redirect('/')
    return redirect('/projects/'+str(p_id))
@login_required    
def report_project(request) :
    
    pass

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
        resultList.append({
            'title': project.title,
            'rate': project.comment_rate,
            'target': project.target,
            'img': project.projectimage_set.first().img.url
        })
    return render(request, 'projects/search_result.html', {'result': result})

    Project.objects.filter(Q(title__icontains="project") | Q(
        details__icontains="project")).distinct().annotate()
