# Create your views here.
from django.http import HttpResponse
from .models import TaskModel
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import TaskForm


@login_required
def index(request):
    tasks_list = TaskModel.objects.all()
    template = loader.get_template('tracker_app/index.html')
    context = {'tasks_list': tasks_list}
    return HttpResponse(template.render(context, request))


@login_required
def detail(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    subtasks = TaskModel.objects.filter(parent=task_id)
    return render(request, 'tracker_app/detail.html', {'task': task, 'subtasks': subtasks})


@login_required
def new_task(request, task_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            if len(TaskModel.objects.filter(id=task_id))>0:
                task.parent = TaskModel.objects.get(id=task_id)
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'tracker_app/task_form.html', {'form': form})


@login_required
def edit_task(request, task_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            TaskModel.objects.filter(pk=task_id).update(title=task.title,
                                                        start_time=task.start_time,
                                                        end_time=task.end_time)
            return redirect('index')
    else:
        task = get_object_or_404(TaskModel, pk=task_id)
        form = TaskForm(instance=task)
    return render(request, 'tracker_app/task_form.html', {'form': form})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    task.delete()
    return HttpResponseRedirect('/')

#===========================================
#   AUTHENTICATION
#===========================================

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'tracker_app/signup.html', {'form': form})


def thanks(request):
    return HttpResponse('Thank you! :)')