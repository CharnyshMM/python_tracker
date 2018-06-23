# Create your views here.
from django.http import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .forms import TaskForm, PlanForm, TaskListViewForm
from .models import TaskModel, PlanModel
from functools import wraps



def access_allowed(function):
    @wraps(function)
    def wrapper(request, task_id, *args, **kwargs):
        user = request.user
        if task_id == '0':
            return function(request, task_id, *args, **kwargs)
        task = TaskModel.objects.get(id=int(task_id))
        if (task.author.id != user.id) and not (user in task.editors.all()):
            return HttpResponse("You can't go there! {}".format(task_id))

        return function(request, task_id, *args, **kwargs)
    return wrapper

@login_required
def index(request):
    tasks_list = TaskModel.select_tasks_by_author(request.user)

    if request.method == "POST":
        form = TaskListViewForm(request.POST)
    else:
        form = TaskListViewForm()

    if form.is_valid():
        if form.cleaned_data['include_shared_tasks']:
            tasks_list = TaskModel.select_tasks_by_editor(request.user)
        tasks_list = tasks_list.order_by(form.cleaned_data['show_mode'])

        if form.cleaned_data['selected_filter'] == 'tags':
            tasks_list = TaskModel.select_tasks_by_tagslist(tasks_list,form.cleaned_data['text_field'])

        else:
            title = " ".join(form.cleaned_data['text_field'])
            tasks_list = tasks_list.filter(title__icontains=title)


    template = loader.get_template('tracker_app/index.html')
    context = {'tasks_list': tasks_list, 'form': form}
    return HttpResponse(template.render(context, request))


@login_required
@access_allowed
def detail(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    editor_names = []
    for editor in task.editors.all():
        editor_names.append(editor.username)

    subtasks = TaskModel.objects.filter(parent=task_id)
    return render(request, 'tracker_app/detail.html', {'task': task, 'subtasks': subtasks, 'editors': editor_names})


@login_required
@access_allowed
def new_task(request, task_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            if task_id != '0':
                task.parent = TaskModel.objects.get(id=task_id)
            task.save()
            users = form.cleaned_data.get('editors')
            print(users)
            for u in users:
                task.editors.add(u)
            task.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'tracker_app/task_form.html', {'form': form})


@login_required
@access_allowed
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
@access_allowed
def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    task.delete()
    return HttpResponseRedirect('/')


@login_required
@access_allowed
def add_plan(request, task_id):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            task = TaskModel.objects.get(id=task_id)
            plan = form.create_plan(task)
            plan.save()
            plan.update()
            return redirect('index')
    else:
        form = PlanForm()
    return render(request, 'tracker_app/plan_form.html', {'form': form})


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