from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^user/$', views.users, name='users'),
    url(r'^user/(?P<request_card_id>[0-9]+)/$', views.user, name='user'),
    url(r'^user/(?P<request_card_id>[0-9]+)/logs$', views.logs, name='user_logs'),
    url(r'^(?P<day>\d{4}-\d{1,2}-\d{1,2})/$', views.day, name='day'),
    url(r'^$', views.index, name='index'),
]