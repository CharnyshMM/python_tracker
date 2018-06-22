from django.db import models
from django.contrib.auth.models import User
from lib.entities.plan import Period

import datetime as dt


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=False)
    editors = models.ManyToManyField(User, related_name='can_edit')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    parent = models.ForeignKey('self', null=True, blank=True)


    def get_parent(self):
        if self.parent:
            return self.parent
        return None

    def get_subtasks(self):
        return TaskModel.objects.filter(parent_task__id=self.id)

    @classmethod
    def add_editor(cls, task_id, user):
        task = cls.objects.get(
            id=task_id
        )
        task.editors.add(user)

    @classmethod
    def remove_editor(cls, task_id, user):
        task = cls.objects.get(
            id=task_id
        )
        task.editors.remove(user)

    @classmethod
    def select_tasks_by_editor(cls, user):
        return TaskModel.objects.filter(editors__id__exact=user.id)

    @classmethod
    def select_tasks_by_author(cls, user):
        return TaskModel.objects.filter(author__id__exact=user.id)

    def __str__(self):
        return self.title


class PlanModel(models.Model):
    task_template = models.ForeignKey(TaskModel, null=False)
    fixed_period = models.CharField(max_length=100, blank=True, null=True)
    timedelta_period = models.DurationField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    created_tasks = models.ManyToManyField(TaskModel, blank=True, related_name='children')

    def get_latest_task(self):
        task = self.created_tasks.last()
        if task is None:
            task = self.task_template
        return task

    def update(self):
        task = self.get_latest_task()
        task.save()
        task.pk = None
        task.start_time = self.increment_dates(task.start_time)
        if task.end_time:
            task.end_time = self.increment_dates(task.end_time)
        self.last_update_time = task.start_time
        task.save()
        self.created_tasks.add(task)


    def increment_dates(self, offset_time):
        if self.fixed_period:
            return Period.add_timedelta(self.fixed_period, offset_time)

        return Period.add_timedelta(self.timedelta_period, offset_time)

    def needs_update(self, cur_time):
        if self.last_update_time is None:
            return True

        if self.end_time is not None:
            if self.last_update_time >= self.end_time:
                return False

        task = self.get_latest_task()
        delta = cur_time - self.increment_dates(self.last_update_time)
        if delta >= dt.timedelta(0):
            return True
        return False
