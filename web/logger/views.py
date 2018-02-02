from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from urllib.parse import unquote, quote
from django.http import HttpResponse
from django.template import loader
from django.forms import formset_factory

from .models import Timelog, User, Team
from .tables import UserTable, DayTable
from .forms import TeamForm

from datetime import datetime, timedelta
from django_tables2 import RequestConfig
from django.db.models import F
from django.contrib.auth.decorators import login_required

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
        'weeks': total_weekly.items()
    }
    return render(request, 'users/detail.html', context)

@login_required(login_url='/admin/login/')
def users(request):
    users = User.objects.all()
    users_sorted = sorted(users, key= lambda u:-u.total_time_limited())
    
    context = {'users': users_sorted}

    return render(request, 'users/index.html', context)

@login_required(login_url='/admin/login/')
def logs(request, request_card_id):
    log_list = Timelog.objects.all().filter(user=request_card_id)
    context = {'log_list': log_list,}

    return render(request, 'users/logs.html', context)

@login_required(login_url='/admin/login/')
def day(request, day):
    day = datetime.strptime(day,'%Y-%m-%d').replace(hour=0, minute=0, second=0, microsecond=0)

    if (request.POST.get('endAll') and request.user.is_authenticated):
        Timelog.objects.filter(end_time=None).update(end_time=F('start_time'))
    elif (request.POST.get('endToday') and request.user.is_authenticated):
        Timelog.objects.filter(end_time=None, start_time__gt=day).update(end_time=F('start_time'))
    else:
        redirect('%s?next=%s' % ('/admin/login/', request.path))

    # get information from database
    log_list = Timelog.objects.all().filter(start_time__gt=day, start_time__lt=day+timedelta(days=1, seconds=-1))

    # calculate total attendance
    logdict = {}
    for log in log_list:
        log.user.first_name = log.user.first_name.capitalize()
        log.user.last_name = log.user.last_name.capitalize()
        if log.end_time != None:
            if log.user in logdict:
                logdict[log.user] += log.delta()
            else:
                logdict[log.user] = log.delta()
        else:
            logdict[log.user] = "Did not check out"
    
    # prepare the table 
    tab_dict = [{"user": usr, "attendance": abse} for usr, abse in logdict.items()]

    table = DayTable(tab_dict)
    RequestConfig(request, paginate={'per_page': 100}).configure(table)

    # variables for navigation
    next_day = (day + timedelta(days=1)).date()
    prev_day = (day + timedelta(days=-1)).date()
    
    context = {
        'next_day': str(next_day),
        'previous_day': str(prev_day),
        'table': table,
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

    return render(request, 'teams/add.html', {'form': form})

@login_required(login_url='/admin/login/')
def teams(request):
    teams = Team.objects.all()
    teams_sorted = sorted(teams, key= lambda t: -t.total_time_limited())
    
    context = {
        'teams': teams_sorted,
    }
    return render(request, 'teams/index.html', context)

@login_required(login_url='/admin/login/')
def team_detail(request, request_team_name):
    team = get_object_or_404(Team, name=unquote(request_team_name))
    users = team.users.all()
    context = {
        'team': team,
        'users': users
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
    