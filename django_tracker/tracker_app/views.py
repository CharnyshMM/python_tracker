# Create your views here.
from django.http import HttpResponse
from .models import TaskModel
from django.template import loader
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .forms import TaskForm


def index(request):
    tasks_list = TaskModel.objects.all()
    template = loader.get_template('tracker_app/index.html')
    context = {'tasks_list': tasks_list,}
    return HttpResponse(template.render(context, request))


def detail(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    return render(request, 'tracker_app/detail.html', {'task': task})


def new_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            task.save()
            return redirect('/')
    else:
        form = TaskForm()
    return render(request, 'tracker_app/task_form.html', {'form': form})


def edit_task(request, task_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            TaskModel.objects.filter(pk=task_id).update(title=task.title, author=task.author)
            return redirect('/')
    else:
        task = get_object_or_404(TaskModel, pk=task_id)
        form = TaskForm(instance=task)
    return render(request, 'tracker_app/task_form.html', {'form': form})

def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    task.delete()
    return HttpResponseRedirect('/')


def thanks(request):
    return HttpResponse('Thank you! :)')