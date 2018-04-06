from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from urllib.parse import unquote, quote
from django.http import HttpResponse
from django.template import loader
from django.forms import formset_factory

from .models import Timelog, User, Team, COMPETITION_START
from .tables import UserTable, DayTable
from .forms import TeamForm

from datetime import datetime, timedelta
from django_tables2 import RequestConfig
from django.db.models import F
from django.contrib.auth.decorators import login_required
import json

@login_required(login_url='/admin/login/')
def index(request):
    return day(request, str(datetime.today().date()))

@login_required(login_url='/admin/login/')
def user(request, request_card_id):
    print(request_card_id)
    user = get_object_or_404(User, card_id=request_card_id)
    total_weekly = user.total_weekly_limited()
    context = {
        'user': user,
        'weeks': total_weekly.items(),
        'title': "User info"
    }
    return render(request, 'users/detail.html', context)

@login_required(login_url='/admin/login/')
def users(request):
    users = User.objects.all()
    users_sorted = sorted(users, key= lambda u:-u.total_time_limited())
    print (COMPETITION_START)
    context = {
        'users': users_sorted,
        'title': "Users",
        'comp_start': COMPETITION_START
    }

    return render(request, 'users/index.html', context)

@login_required(login_url='/admin/login/')
def logs(request, request_card_id):
    if (request.POST.get("endLog") and request.user.is_authenticated):
        log = Timelog.objects.get(id=request.POST.get("endLogId"))
        log.end_time = datetime.now()
        log.save()
    elif (request.POST.get("deleteLog") and request.user.is_authenticated):
        log = Timelog.objects.get(id=request.POST.get("endLogId"))
        log.delete()

    log_list = Timelog.objects.all().filter(user=request_card_id)
    context = {'log_list': log_list,}

    return render(request, 'users/logs.html', context)

@login_required(login_url='/admin/login/')
def day(request, day):
    day = datetime.strptime(day,'%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)
    searchResult = None
    if (request.POST.get('endAll') and request.user.is_authenticated):
        Timelog.objects.filter(end_time=None).update(end_time=F('start_time'))
    elif (request.POST.get('endToday') and request.user.is_authenticated):
        Timelog.objects.filter(end_time=None, start_time__gt=day, start_time__lt=day+timedelta(1)).update(end_time=F('start_time'))
    elif (request.POST.get('searchUser') and request.user.is_authenticated):
        searchResult = User.objects.filter(first_name = request.POST.get('searchName'))
    elif (request.POST.get('addLog') and request.user.is_authenticated):
        log = Timelog()
        log.user = User.objects.get(card_id = request.POST.get('addLogId'))
        log.start_time = datetime.now()
        log.save()
    elif (request.POST.get('endLog') and request.user.is_authenticated):
        log = Timelog.objects.get(id)
    else:
        redirect('%s?next=%s' % ('/admin/login/', request.path))

    # get information from database
    log_list = Timelog.objects.all().filter(start_time__gt=day, start_time__lt=day+timedelta(days=1, seconds=-1))

    # calculate total attendance
    logdict = {}
    for log in log_list:
        log.user.first_name = log.user.first_name.capitalize()
        log.user.last_name = log.user.last_name.capitalize()

        if log.end_time == None:
            endtime = "Did not check out"
            delta = timedelta(0)
        else:
            endtime = log.end_time
            delta = log.delta()

        if log.user in logdict:
            logdict[log.user]["att"] += int(delta.total_seconds()/60)
            logdict[log.user]["starttimes"].append(log.start_time)
            logdict[log.user]["endtimes"].append(endtime) 
        else:
            logdict[log.user] = {"att": int(log.delta().total_seconds()/60), "starttimes": [log.start_time], "endtimes": [endtime]}
    
    # prepare the table 
    tab_dict = [{"user": usr, "attendance": data["att"], "starttimes": data["starttimes"], "endtimes": data["endtimes"]} for usr, data in logdict.items()]

    table = DayTable(tab_dict)
    RequestConfig(request, paginate={'per_page': 100}).configure(table)

    # variables for navigation
    next_day = (day + timedelta(days=1)).date()
    prev_day = (day + timedelta(days=-1)).date()
    
    context = {
        'next_day': str(next_day),
        'previous_day': str(prev_day),
        'today': day,
        'table': table,
        'searchResult': searchResult,
        'title': "Logs Today"
    }

    return render(request, 'logs/index.html', context)

@login_required(login_url='/admin/login/')
def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            users = form.cleaned_data['users']

            team = Team()
            team.name = name
            team.save()
            team.users.set(users)
            team.save()
            return HttpResponse(name + " " + str([str(user) for user in users]))
    else: 
        form = TeamForm()

    context = {
        'form': form,
        'title': "Add team"
    }
    return render(request, 'teams/add.html', context)

@login_required(login_url='/admin/login/')
def teams(request):
    teams = Team.objects.all()
    teams_sorted = sorted(teams, key= lambda t: -t.total_time_limited())
    
    context = {
        'teams': teams_sorted,
        'title': "Teams",
        'comp_start': COMPETITION_START
    }
    return render(request, 'teams/index.html', context)

@login_required(login_url='/admin/login/')
def team_detail(request, request_team_name):
    team = get_object_or_404(Team, name=unquote(request_team_name))
    users = team.users.all()
    context = {
        'team': team,
        'users': users,
        'title': "Team info"
    }
    return render(request, 'teams/detail.html', context)

@login_required(login_url='/admin/login/')
def edit_team(request, request_team_name):
    team = get_object_or_404(Team, name=unquote(request_team_name))
    form = TeamForm(initial={
        'name': team.name,
        'Members': team.users,
    })
    context = {
        'team': team,
        'form': form,
        'title': "Edit team"
    }
    return render(request, 'teams/edit.html', context)

@login_required(login_url='/admin/login/')
def update_team(request, request_team_name):
    if request.method == 'POST':
        team = get_object_or_404(Team, name=unquote(request_team_name))
        form = TeamForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            users = form.cleaned_data['users']
            team.name = name
            team.users.set(users)
            team.save()
            return HttpResponse(name + " updated")
        else: 
            return HttpResponse("form not valid " + str(form.errors))

@login_required(login_url='/admin/login')
def _class(request, name):
    class_name = unquote(name)
    users = User.objects.all().filter(class_field=class_name)
    users = sorted(users, key = lambda u:-u.total_time_limited())
    context = {
        'users': users,
        'name': class_name,
        'title': "Class info " + class_name,
    }
    return render(request, 'classes/detail.html', context)

@login_required(login_url='/admin/login')
def _classes(request):
    classes = User.objects.all().values('class_field').distinct()
    classes = sorted(classes, key = lambda c: c['class_field'])
    context = {
        'classes': classes,
        'title': "Classes"
    }
    return render(request, 'classes/index.html', context)

