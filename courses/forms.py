from django import forms

from courses.models import Teacher


class CreateCourseForm(forms.Form):
    name = forms.CharField(max_length=200)
    description = forms.CharField(widget=forms.Textarea)


class CreateGroupForm(forms.Form):
    tag = forms.CharField(max_length=15)
    size = forms.IntegerField()
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all(), empty_label=None)