from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import datetime
from django.forms import SelectDateWidget
from courses.models import Teacher
from django.core.validators import RegexValidator

DEGREE_CHOICES = [
    (1, 'inż.'),
    (2, 'mgr'),
    (3, 'mgr inż.'),
    (4, 'dr'),
    (5, 'dr inż'),
    (7, 'dr hab.'),
]


def check_degree(degree):
    if degree is None:
        raise forms.ValidationError("Select your academic degree")

#
# def check_index_length(index):
#     if len(index) < 6:
#         raise forms.ValidationError("Index to short")


class SignUpStudentForm(UserCreationForm):
    index_no = forms.CharField(max_length=30, help_text='Required.',
                               validators=[RegexValidator(regex="^\d{6}$", message="Index should be 6 digits number", )])
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'index_no', 'password1', 'password2')


class SignUpTeacherForm(UserCreationForm):
    academic_degree = forms.CharField(widget=forms.Select(choices=DEGREE_CHOICES),
                                      help_text='Required.', validators=[check_degree, ])
    last_name = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)


    class Meta:
        model = User
        fields = ('username', 'last_name', 'first_name', 'academic_degree', 'password1', 'password2')


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
