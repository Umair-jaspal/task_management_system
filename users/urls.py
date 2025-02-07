from django.urls import path
from . import views
from .views import logout_view

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', logout_view, name='logout'),
    # Add other URLs like login here if needed
]
