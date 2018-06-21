from django import forms
from .models import TaskModel


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = '__all__'
        widgets = {
            'start_time': forms.DateTimeInput(),
            'end_time': forms.DateTimeInput()
        }
