from django.contrib import admin

from .models import Timelog, User, Team

admin.site.register(Timelog)
admin.site.register(User)
admin.site.register(Team)