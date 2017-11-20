from django.contrib import admin

from .models import Timelog, User

admin.site.register(Timelog)
admin.site.register(User)