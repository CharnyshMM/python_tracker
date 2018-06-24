# Create your views here.
from django.db.models import Q
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
from django.utils import timezone
import datetime as dt


def check_permissions(model):
    def real_decorator(function):
        @wraps(function)
        def wrapper(request, object_id, *args, **kwargs):
            user = request.user
            if object_id == '0':
                return function(request, object_id, *args, **kwargs)
            obj = get_object_or_404(klass=model, pk=object_id)
            if not obj.user_can_access(request.user):
                return HttpResponse("You can't go there! {}".format(object_id))

            return function(request, object_id, *args, **kwargs)
        return wrapper
    return real_decorator


@login_required
def index(request):
    tasks_list = TaskModel.select_tasks_by_editor(request.user)

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
def actuals(request):
    for plan in PlanModel.objects.all():
        plan.update()

    tasks_list = TaskModel.select_tasks_by_editor(request.user)
    report_time = timezone.now()
    time_range = (report_time - dt.timedelta(minutes=3), report_time + dt.timedelta(minutes=3))
    starting_tasks = tasks_list.filter(start_time__range=time_range)
    ending_tasks = tasks_list.filter(end_time__range=time_range)
    continuing_tasks = tasks_list.filter(start_time__lt=time_range[0], end_time__gt=time_range[1])
    return render(request,
                  'tracker_app/actuals.html',
                    {'starting_tasks': starting_tasks,
                     'continuing_tasks': continuing_tasks,
                     'ending_tasks': ending_tasks,
                    }
                  )

@login_required
@check_permissions(model=TaskModel)
def detail(request, object_id):
    task = get_object_or_404(TaskModel, pk=object_id)
    editor_names = []
    for editor in task.editors.all():
        editor_names.append(editor.username)
    template_for_plan = PlanModel.objects.filter(task_template=task).first()
    created_by_plan = PlanModel.objects.filter(created_tasks=task).first()
    subtasks = TaskModel.objects.filter(parent=object_id)
    return render(request,
                  'tracker_app/detail.html',
                  {'task': task,
                   'subtasks': subtasks,
                   'editors': editor_names,
                   'template_for_plan': template_for_plan,
                   'created_by_plan':created_by_plan,
                   }
                  )


@login_required
@check_permissions(TaskModel)
def new_task(request, object_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.author = request.user
            if object_id != '0':
                task.parent = TaskModel.objects.get(id=object_id)
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
@check_permissions(TaskModel)
def edit_task(request, object_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            TaskModel.objects.filter(pk=object_id).update(title=task.title,
                                                          start_time=task.start_time,
                                                          end_time=task.end_time)
            return redirect('index')
    else:
        task = get_object_or_404(TaskModel, pk=object_id)

        form = TaskForm(instance=task)
    return render(request, 'tracker_app/task_form.html', {'form': form})


@login_required
@check_permissions(TaskModel)
def delete_task(request, task_id):
    task = get_object_or_404(TaskModel, pk=task_id)
    template_for_plan = PlanModel.objects.filter(task_template=task)
    if len(template_for_plan) > 0:
        return HttpResponse("This task is a template for plan! You can't delete it before deleting plan")
    task.delete()
    return HttpResponseRedirect('/')


@login_required
@check_permissions(TaskModel)
def add_plan(request, object_id):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            task = get_object_or_404(TaskModel, pk=object_id)
            plan = form.create_plan(task)
            plan.author = request.user
            plan.save()
            plan.update()
            return redirect('index')
    else:
        form = PlanForm()
    return render(request, 'tracker_app/plan_form.html', {'form': form})


@login_required
def all_plans(request):
    plans_list = PlanModel.objects.filter(author=request.user)
    return render(request, 'tracker_app/plans.html', {'plans_list': plans_list})


@login_required
@check_permissions(PlanModel)
def plan_details(request, object_id):
    plan = get_object_or_404(PlanModel,pk=object_id)
    return render(request, 'tracker_app/plan_details.html', {'plan': plan})


@login_required
@check_permissions(PlanModel)
def delete_plan(request, object_id):
    plan = get_object_or_404(PlanModel,pk=object_id)
    plan.delete()
    return HttpResponseRedirect('all_plans')


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