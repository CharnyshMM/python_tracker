

from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    # /tracker_app
    url(r'^$', views.index, name='index'),
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'tracker_app/login.html'}, name='login'),
    url(r'^accounts/logout/$', auth_views.logout,{'template_name': 'tracker_app/logout.html'}, name='logout'),
    url(r'^accounts/signup/$', views.signup, name='signup'),
    # /tracker_app/task/5
    url(r'^task/(?P<task_id>\d+)/$', view=views.detail, name='detail_task'),
    # /tracker_app/task/new
    url(r'^task/(?P<task_id>\d+)/new/$', view=views.new_task, name='new_task'),
    # /tracker_app/task/5/edit
    url(r'^task/(?P<task_id>\d+)/edit/$', view=views.edit_task, name='edit_task'),
    url(r'^task/(?P<task_id>\d+)/delete/$', view=views.delete_task, name='delete_task'),
    url(r'^task/(?P<task_id>\d+)/new_plan/$',view=views.add_plan, name='new_plan'),
    # /tracker_app/thanks
    url(r'^thanks/$', view=views.thanks, name='thanks'),
]
