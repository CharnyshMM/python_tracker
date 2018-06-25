

from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    # /tracker_app
    url(r'^$', view=views.index, name='index'),
    url(r'^actuals/$',view=views.actuals, name='actuals'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'tracker_app/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,{'template_name': 'tracker_app/logout.html'}, name='logout'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    # /tracker_app/task/5
    url(r'^tasks/(?P<object_id>\d+)/$', view=views.task_details, name='detail_task'),

    url(r'^tasks/(?P<object_id>\d+)/new_reminder/$', view=views.add_reminder, name='add_reminder'),
    url(r'^tasks/(?P<object_id>\d+)/status/$', view=views.task_status, name='task_status'),
    url(r'^reminders/(?P<object_id>\d+)/delete/$',view=views.delete_reminder, name='delete_reminder'),
    # /tracker_app/task/new
    url(r'^tasks/(?P<object_id>\d+)/new/$', view=views.new_task, name='new_task'),
    # /tracker_app/task/5/edit
    url(r'^tasks/(?P<object_id>\d+)/edit/$', view=views.edit_task, name='edit_task'),
    url(r'^tasks/(?P<object_id>\d+)/delete/$', view=views.delete_task, name='delete_task'),
    url(r'^tasks/(?P<object_id>\d+)/new_plan/$',view=views.add_plan, name='new_plan'),
    url(r'^plans/(?P<object_id>\d+)/$', view=views.plan_details, name='plan_details'),
    url(r'^plans/(?P<object_id>\d+)/delete/$',view=views.delete_plan, name='delete_plan'),
    # /tracker_app/plans
    url(r'^plans/', view=views.all_plans, name='all_plans'),
    # /tracker_app/thanks
    url(r'^thanks/$', view=views.thanks, name='thanks'),
]
