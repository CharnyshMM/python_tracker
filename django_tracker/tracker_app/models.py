from django.db import models

# Create your models here.
from django.contrib.auth.models import User

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
        task.users.add(user)

    @classmethod
    def remove_editor(cls, task_id, user):
        task = cls.objects.get(
            id=task_id
        )
        task.users.remove(user)






