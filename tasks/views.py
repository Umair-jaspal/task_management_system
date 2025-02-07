from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Task, Project
from django.urls import reverse_lazy
from .forms import TaskForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'

class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'status']
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')



@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
@user_passes_test(lambda u: u.role == 'admin')
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign task to the logged-in user
            task.save()
            return redirect('task_list')  # Redirect back to task list after adding
    else:
        form = TaskForm()
    return render(request, 'tasks/add_task.html', {'form': form})

def view_tasks(request):
    tasks = Task.objects.all()  # Fetch tasks based on user or all tasks
    return render(request, 'tasks/view_tasks.html', {'tasks': tasks})

def edit_task(request, task_id):  # Change 'id' to 'task_id' to match URL
    task = get_object_or_404(Task, id=task_id, user=request.user)  # Ensure parameter name matches
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')  # Redirect after saving
    else:
        form = TaskForm(instance=task)  # Load existing task details
    return render(request, 'tasks/edit_task.html', {'form': form})

def delete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == "POST":
        task.delete()
        return redirect('view_tasks')
    return render(request, 'tasks/delete_task.html', {'task': task})