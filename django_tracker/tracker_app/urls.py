

from . import views
from django.conf.urls import url

urlpatterns = [
    # /tracker_app
    url(r'^$', views.index, name='index'),
    # /tracker_app/task/5
    url(r'^task/(?P<task_id>[0-9]+)/$', view=views.detail, name='detail_task'),
    # /tracker_app/task/new
    url(r'^task/new/$', view=views.new_task, name='new_task'),
    # /tracker_app/task/5/edit
    url(r'^task/(?P<task_id>\d+?)/edit/$', view=views.edit_task, name='edit_task'),
    url(r'^task/(?P<task_id>\d+?)/delete/$', view=views.delete_task, name='delete_task'),
    # /tracker_app/thanks
    url(r'^thanks/$', view=views.thanks, name='thanks'),
]
