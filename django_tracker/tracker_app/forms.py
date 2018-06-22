from django import forms
from .models import TaskModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re

class MyMultiChoiceField(forms.CharField):
    def to_python(self, value):
        usernames = re.findall(r'(\w+)\W*',value)
        users = []
        try:
            for u in usernames:
                user = User.objects.get(username=u)
                users.append(user)
        except ObjectDoesNotExist:
            raise ValidationError('username incorrect')
        return users

class TaskForm(forms.ModelForm):
    editors = MyMultiChoiceField(required=False)
    class Meta:
        model = TaskModel
        fields = ('title','start_time','end_time')
        widgets = {
            'start_time': forms.DateTimeInput(),
            'end_time': forms.DateTimeInput(),
        }


