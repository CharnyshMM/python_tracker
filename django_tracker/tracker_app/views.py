# Create your views here.

from django.http import HttpResponse
from django.template import loader

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import TaskForm, PlanForm, ReminderForm
from .models import TaskModel, PlanModel, ReminderModel
from functools import wraps
from django.utils import timezone
import datetime as dt
import re


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
    tasks_list = TaskModel.select_tasks_by_editor(request.user).distinct()

    key = request.GET.get('key')
    query = request.GET.get('query')
    order = request.GET.get('order')
    active_only = request.GET.get("active_only")
    tops_only = request.GET.get("tops_only")
    if tops_only:
        tasks_list = tasks_list.filter(parent=None)
    if active_only:
        tasks_list = tasks_list.filter(active=True)
    if order is None:
        order='priority'
    if query:
        if key == 'tags':
            tasks_list = TaskModel.filter_by_tags(re.findall(r'(\w+)\W*',query))
        else:
            tasks_list = tasks_list.filter(title__icontains=query)
    tasks_list = tasks_list.order_by(order)

    template = loader.get_template('tracker_app/index.html')
    context = {'tasks_list': tasks_list}
    return HttpResponse(template.render(context, request))


@login_required
def actuals(request):
    for plan in PlanModel.objects.all():
        plan.update()

    tasks_list = TaskModel.select_tasks_by_editor(request.user).filter(active=True)
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
def task_details(request, object_id):
    task = get_object_or_404(TaskModel, pk=object_id)
    editor_names = []
    for editor in task.editors.all():
        editor_names.append(editor.username)
    template_for_plan = PlanModel.objects.filter(task_template=task).first()
    created_by_plan = PlanModel.objects.filter(created_tasks=task).first()
    subtasks = TaskModel.objects.filter(parent__id=object_id)
    reminders = ReminderModel.objects.filter(task__id=object_id)
    return render(request,
                  'tracker_app/detail.html',
                  {'task': task,
                   'subtasks': subtasks,
                   'editors': editor_names,
                   'template_for_plan': template_for_plan,
                   'created_by_plan':created_by_plan,
                   'reminders':reminders,
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
            form.save_m2m()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'tracker_app/task_form.html', {'form': form})

@login_required
@check_permissions(TaskModel)
def add_reminder(request, object_id):
    task = get_object_or_404(TaskModel,pk=object_id)
    if request.method == "POST":
        form = ReminderForm(request.POST)
        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.task = task
            reminder.save()
            return task_details(request, task.id)
    else:
        form = ReminderForm()
        return render(request, 'tracker_app/reminder_form.html', {'form': form, 'task_title': task.title})

@login_required

def delete_reminder(request, object_id):
    reminder = get_object_or_404(ReminderModel, pk=object_id)
    task_id = reminder.task.id
    reminder.delete()
    return task_details(request, task_id)


@login_required
@check_permissions(TaskModel)
def edit_task(request, object_id):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():

            task = form.save(commit=False)
            task.id = object_id
            task.save(update_fields=('title','start_time','end_time','priority'))
            form.save_m2m()
            return redirect('index')
    else:
        task = get_object_or_404(TaskModel, pk=object_id)

        form = TaskForm(instance=task)
    return render(request, 'tracker_app/task_form.html', {'form': form})


@login_required
@check_permissions(TaskModel)
def delete_task(request, object_id):
    print("it deletes")
    task = get_object_or_404(TaskModel, pk=object_id)
    template_for_plan = PlanModel.objects.filter(task_template=task)
    if len(template_for_plan) > 0:
        return HttpResponse("This task is a template for plan! You can't delete it before deleting plan")
    task.delete()
    return HttpResponseRedirect('/')



@login_required
@check_permissions(TaskModel)
def task_status(request, object_id):
    task = get_object_or_404(TaskModel, pk=object_id)
    task.active = not task.active
    task.save()

    return redirect("index")


@login_required
@check_permissions(TaskModel)
def add_plan(request, object_id):
    task = get_object_or_404(TaskModel, pk=object_id)
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            plan = form.create_plan(task)
            plan.author = request.user
            plan.save()
            plan.update()
            return redirect('index')
    else:

        form = PlanForm()
    return render(request, 'tracker_app/plan_form.html', {'form': form, 'task_title':task.title})


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