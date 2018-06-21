from django.db import models

# Create your models here.


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)



