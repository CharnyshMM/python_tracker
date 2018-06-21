from django import forms
from .models import TaskModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskModel
        fields = ('title','start_time','end_time', 'editors')
        widgets = {
            'start_time': forms.DateTimeInput(),
            'end_time': forms.DateTimeInput()
        }
