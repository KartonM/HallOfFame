from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import SelectDateWidget
from courses.models import Teacher, Student

DEGREE_CHOICES = [
    (1, 'inż.'),
    (2, 'dr'),
    (3, 'dr inż'),
    (4, 'mgr'),
    (5, 'dr hab.'),
]


class SignUpStudentForm(UserCreationForm):
    index_no = forms.CharField(max_length=30, help_text='Required.')
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'index_no', 'password1', 'password2', 'username')


class SignUpTeacherForm(UserCreationForm):
    academic_degree = forms.CharField(widget=forms.Select(choices=DEGREE_CHOICES), help_text='Required.')
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'academic_degree', 'password1', 'password2', 'username')


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


class RegisterTaskPointsForm(forms.Form):
    points = forms.IntegerField(initial=0, min_value=0)

    # def __init__(self, *args, **kwargs):
    #     max_points = kwargs.pop('max_points')
    #     super(RegisterTaskPointsForm, self).__init__(*args, **kwargs)
    #     self.fields['points'].max_value = max_points


class PickStudentForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())

    def __init__(self, *args, **kwargs):
        if 'students_choice_set' in kwargs:
            students_choice_set = kwargs.pop('students_choice_set')
            super(PickStudentForm, self).__init__(*args, **kwargs)
            self.fields['student'].queryset = students_choice_set
        else:
            super(PickStudentForm, self).__init__(*args, **kwargs)


class FileUploadForm(forms.Form):
    file = forms.FileField()
