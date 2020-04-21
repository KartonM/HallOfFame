from datetime import datetime

from django import forms
from django.forms import SelectDateWidget

from courses.models import Teacher


class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)


class CreateGroupForm(forms.Form):
    tag = forms.CharField(max_length=15)
    size = forms.IntegerField()
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None)


class CreateEventForm(forms.Form):
    name = forms.CharField(max_length=100)
    date = forms.DateTimeField(widget=SelectDateWidget(), initial=datetime.now())
    is_required_to_pass_the_course = forms.BooleanField(required=False)
    min_tasks_positive = forms.IntegerField(initial=0)
    weight = forms.IntegerField(initial=1)
    tasks_count = forms.IntegerField(initial=0)


class CreateTaskForm(forms.Form):
    name = forms.CharField(max_length=100)
    max_points = forms.IntegerField()
