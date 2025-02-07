from django.contrib import admin
from .models import Task, Project  # Register your task and project models

admin.site.register(Task)
admin.site.register(Project)
