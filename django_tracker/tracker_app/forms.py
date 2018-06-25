from django import forms
from .models import TaskModel, PlanModel, Priority
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re


class CommaSepMultiWordsCharField(forms.CharField):
    def to_python(self, value):
        return re.findall(r'(\w+)\W*',value)


def usernames_to_users(usernames):
    users = []
    try:
        for u in usernames:
            user = User.objects.get(username=u)
            users.append(user)
    except ObjectDoesNotExist:
        raise ValidationError('username incorrect')
    return users


class TaskForm(forms.ModelForm):

    class Meta:
        model = TaskModel
        fields = ('title','start_time','end_time','priority','tags', 'editors')
        widgets = {
            'priority': forms.Select(choices=Priority.PRIORITY_CHOICES),
            'editors': forms.SelectMultiple(attrs={'id':'select_editors'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        end_time = cleaned_data.get("end_time")
        start_time = cleaned_data.get("start_time")
        if start_time >= end_time:
            msg = "Task start time can't be greater than end time!"
            self.add_error("start_time", msg)




class PlanForm(forms.Form):
    periods = ['yearly','monthly','daily']
    fixed_period = forms.ChoiceField(choices=[(p,p) for p in periods],required=False)
    mode = forms.ChoiceField(choices=[('fixed', 'fixed'), ('custom', 'custom')])
    custom_period=forms.DurationField(required=False)
    end_time = forms.DateTimeField(required=False)


    def get_mode(self):
        return self.cleaned_data['mode']

    def get_period(self):
        if self.get_mode() == 'fixed':
            return self.cleaned_data['fixed_period']
        else:
            return self.cleaned_data['custom_period']

    def create_plan(self,task_template):
        self.clean()
        if self.get_mode()=='fixed':
            return PlanModel(task_template=task_template,
                             fixed_period=self.get_period(),
                            end_time=self.cleaned_data['end_time'])

        return PlanModel(task_template=task_template,
                         timedelta_period=self.get_period(),
                         end_time=self.cleaned_data['end_time'])

