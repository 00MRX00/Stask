from django.contrib import admin

from .models import User, UserLogPass

admin.site.register(User)
admin.site.register(UserLogPass)