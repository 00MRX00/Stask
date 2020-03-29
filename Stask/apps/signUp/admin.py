from django.contrib import admin

from .models import User, UserLogPass, Project, ProjectUsers, Task, TaskUsers, Todo

admin.site.register(User)
admin.site.register(UserLogPass)
admin.site.register(Project)
admin.site.register(ProjectUsers)
admin.site.register(Task)
admin.site.register(TaskUsers)
admin.site.register(Todo)