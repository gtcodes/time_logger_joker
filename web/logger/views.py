from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from logger.models import Timelog, User
from logger.tables import UserTable, DayTable
from datetime import datetime, timedelta
from django_tables2 import RequestConfig
from django.db.models import F
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return day(request, str(datetime.today().date()))


@login_required(login_url='/admin/login/')
def user(request, request_card_id):
    user = get_object_or_404(User, card_id=request_card_id)
    context = {'user': user,}
    return render(request, 'users/detail.html', context)

@login_required(login_url='/admin/login/')
def users(request):
    user_list = User.objects.all()
    table = UserTable(user_list)
    RequestConfig(request).configure(table)
    context = {'table': table}

    return render(request, 'users/index.html', context)

@login_required(login_url='/admin/login/')
def logs(request, request_card_id):
    log_list = Timelog.objects.all().filter(user=request_card_id)
    context = {'log_list': log_list,}

    return render(request, 'users/logs.html', context)

def day(request, day):
    print("##########################")
    print("request", request.user.is_authenticated)
    print("##########################")
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
    RequestConfig(request).configure(table)

    # variables for navigation
    next_day = (day + timedelta(days=1)).date()
    prev_day = (day + timedelta(days=-1)).date()
    
    context = {
        'next_day': str(next_day),
        'previous_day': str(prev_day),
        'table': table,
    }

    return render(request, 'logs/index.html', context)