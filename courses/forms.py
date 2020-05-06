from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
