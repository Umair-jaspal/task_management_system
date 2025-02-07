from django.shortcuts import render, redirect
from .forms import RegistrationForm
from tasks.models import Task
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import logout


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def home(request):
    tasks = Task.objects.filter(user=request.user)  # Only tasks for the logged-in user
    return render(request, 'users/home.html', {'tasks': tasks})

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')
