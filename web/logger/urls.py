from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^user/', include([
        url(r'^(?P<request_card_id>[0-9]+)/logs$', views.logs, name='user_logs'),
        url(r'^(?P<request_card_id>[0-9]+)/$', views.user, name='user'),
        url(r'^', views.users, name='users'),
    ])),
    url(r'^team/', include([
        url(r'^add$', views.add_team, name='add_team'),
        url(r'^(?P<request_team_name>[0-9A-Za-z\!\?\#\\\/\(\)\-\_\+\$\<\>\,\.\'\%\& ]+)$', views.team_detail, name='team_detail'),
        url(r'^', views.teams, name='teams'),
    ])),
    url(r'^(?P<day>\d{4}-\d{1,2}-\d{1,2})/$', views.day, name='day'),
    url(r'^$', views.index, name='index'),
]