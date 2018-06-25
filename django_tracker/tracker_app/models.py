from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from lib.entities.plan import Period

from taggit.managers import TaggableManager
import datetime as dt


class Priority:
    LOW = 3
    MEDIUM = 2
    HIGH = 1
    PRIORITY_CHOICES = (
        (LOW,'low'),
        (MEDIUM, 'medium'),
        (HIGH,'high'),
    )


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, null=False)
    editors = models.ManyToManyField(User, related_name='can_edit', blank=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    priority = models.IntegerField(choices=Priority.PRIORITY_CHOICES, default=Priority.MEDIUM)
    tags = TaggableManager(blank=True, help_text='input tags separated with spaces or commas')
    active = models.BooleanField(default=True)

    def get_parent(self):
        if self.parent:
            return self.parent
        return None

    def get_subtasks(self):
        return TaskModel.objects.filter(parent_task__id=self.id)


    @classmethod
    def select_tasks_by_editor(cls, user):
        query = Q(editors__id__exact=user.id) | Q(author__id__exact=user.id)
        return TaskModel.objects.filter(query)

    @classmethod
    def select_tasks_by_author(cls, user):
        return TaskModel.objects.filter(author__id__exact=user.id)

    @classmethod
    def filter_by_tags(cls, tagslist):
        query = None
        for tag in tagslist:
            print(tag)
            if not query:
                query = Q(tags__name__in=[tag])
            query = query and Q(tags__name__in=[tag])
        return cls.objects.filter(query)

    def user_can_access(self,user):
        if self.author.id == user.id or user in self.editors.all() > 0:
            return True
        return False

    def __str__(self):
        return self.title

class ReminderModel(models.Model):
    task = models.ForeignKey(TaskModel, blank=True, null=False)
    alert_time = models.DateTimeField(null=False)
    dismissed = models.BooleanField(default=False)

class PlanModel(models.Model):
    task_template = models.ForeignKey(TaskModel, null=False)
    author = models.ForeignKey(User, null=False)
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
        while self.needs_update(timezone.now()):
            task = self.get_latest_task()
            reminders = ReminderModel.objects.filter(task=task)
            task.save()
            task.pk = None
            task.start_time = self.increment_dates(task.start_time)
            task.end_time = self.increment_dates(task.end_time)
            for r in reminders:
                r.pk = None
                r.alert_time = self.increment_dates(r.alert_time)
                r.save()
            self.last_update_time = task.start_time
            task.save()
            self.created_tasks.add(task)
            self.save()

    def increment_dates(self, offset_time):
        return Period.add_timedelta(self.period, offset_time)

    @property
    def period(self):
        if self.fixed_period:
            return self.fixed_period
        return self.timedelta_period


    def needs_update(self, cur_time):
        if self.last_update_time is None:
            return True
        if self.end_time is not None:
            if self.last_update_time >= self.end_time:
                return False
        delta = cur_time - self.increment_dates(self.last_update_time)
        if delta >= dt.timedelta(0):
            return True
        return False

    def user_can_access(self,user):
        if self.author.id == user.id:
            return True
        return False