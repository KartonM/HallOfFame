from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from courses.forms import SignUpStudentForm, SignUpTeacherForm


# Create your views here.
from courses.models import Course


def index(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses/index.html', context)


def blank(request):
    return render(request, 'courses/blank.html')


def pick_register(request):
    return render(request, 'registration/pickRegister.html')


def signup_student(request):
    if request.method == 'POST':
        form = SignUpStudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.student.index_no = form.cleaned_data.get('index_no')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/courses')
    else:
        form = SignUpStudentForm()
    return render(request=request,
                  template_name='registration/register.html',
                  context={'form': form})


def signup_teacher(request):
    if request.method == 'POST':
        form = SignUpTeacherForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.teacher.academic_degree = form.cleaned_data.get('academic_degree')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/courses')
    else:
        form = SignUpTeacherForm()
    return render(request=request,
                  template_name='registration/register.html',
                  context={'form': form})
