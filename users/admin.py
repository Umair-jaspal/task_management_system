from django.contrib import admin
from .models import CustomUser  # If you have a custom user model

admin.site.register(CustomUser)
