from django import forms
from .models import TaskModel, PlanModel, Priority
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import re


class CommaSepMultiWordsCharField(forms.CharField):
    def to_python(self, value):
        return re.findall(r'(\w+)\W*',value)

class CommaSepMultiUserField(CommaSepMultiWordsCharField):
    def to_python(self, value):
        usernames = super().to_python(value)
        users = []
        try:
            for u in usernames:
                user = User.objects.get(username=u)
                users.append(user)
        except ObjectDoesNotExist:
            raise ValidationError('username incorrect')
        return users


class TaskForm(forms.ModelForm):
    editors = CommaSepMultiUserField(required=False)
    class Meta:
        model = TaskModel
        fields = ('title','start_time','end_time','priority','tags')
        widgets = {
            'priority': forms.RadioSelect(choices=Priority.PRIORITY_CHOICES)
        }


class PlanForm(forms.Form):
    periods = ['yearly','monthly','daily']
    fixed_period = forms.ChoiceField(choices=[(p,p) for p in periods],required=False)
    mode = forms.ChoiceField(choices=[('fixed', 'fixed'), ('custom', 'custom')],widget=forms.RadioSelect)
    custom_period=forms.DurationField(required=False)
    end_time = forms.DateTimeField(required=False)


    def get_mode(self):
        return self.cleaned_data['mode']

    def get_period(self):
        if self.get_mode() == 'fixed':
            print('fixed')
            return self.cleaned_data['fixed_period']
        else:
            return self.cleaned_data['custom_period']

    def create_plan(self,task_template):
        self.clean()
        period = None
        if self.get_mode()=='fixed':
            return PlanModel(task_template=task_template,
                             fixed_period=self.get_period(),
                            end_time=self.cleaned_data['end_time'])

        return PlanModel(task_template=task_template,
                         timedelta_period=self.get_period(),
                         end_time=self.cleaned_data['end_time'])


class TaskListViewForm(forms.Form):
    show_modes = ['priority', 'start_time', 'end_time', 'notifications']
    filters = ['tags', 'title']
    include_shared_tasks = forms.BooleanField(initial=True, label='Include shared tasks',required=False)
    show_mode = forms.ChoiceField(choices=[(m, m) for m in show_modes], required=False)
    selected_filter = forms.ChoiceField(choices=[(f, f) for f in filters])
    text_field = CommaSepMultiWordsCharField(max_length=100, required=False)
