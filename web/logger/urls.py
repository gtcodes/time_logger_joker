from django.conf.urls import include
from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    # user paths
    re_path('user/(?P<request_card_id>[0-9]+)/logs/', views.logs, name='user_logs'),
    re_path('user/(?P<request_card_id>[0-9]+)/', views.user, name='user'),
    path('user/', views.users, name='users'),
    
    # team paths
    path('team/', include([
        re_path('(?P<request_team_name>[0-9A-Za-z\!\?\#\(\)\-\_\+\$\<\>\,\.\'\%\& ]+)/', include([
            path('edit/', views.edit_team, name='edit_team'),
            path('update/', views.update_team, name='update_team'),
            path('', views.team_detail, name='team_detail'),
        ])),
        path('add/', views.add_team, name='add_team'),
        path('',views.teams, name='teams'),
    ])),

    # logger
    re_path('(?P<day>\d{4}-\d{1,2}-\d{1,2})', views.day, name='day'),
    path('', views.index, name='index'),

    path('class/<str:name>/', views._class, name='class'),
    path('class/', views._classes, name='classes'),
]