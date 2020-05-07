from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from courses.forms import SignUpStudentForm, SignUpTeacherForm


# Create your views here.
from courses.models import Course, Teacher, Group, Event, Task
from courses.forms import CreateCourseForm, CreateGroupForm, CreateEventForm, CreateTaskForm
from django.forms import formset_factory


def index(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses/index.html', context)


def blank(request):
    return render(request, 'courses/blank.html')


def create_course(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                tutor=Teacher.objects.first()  # TODO use id of logged in teacher instead
            )
            return HttpResponseRedirect(f'{course.id}')
    else:
        form = CreateCourseForm()

    return render(request, 'courses/add_course.html', {'form': form})


def course(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'courses/course.html', {'course': course})


def create_group(request, course_id):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            Group.objects.create(
                tag=form.cleaned_data['tag'],
                size=form.cleaned_data['size'],
                course_id=course_id,
                teacher=form.cleaned_data['teacher']
            )
            return HttpResponseRedirect(f'/courses/{course_id}')
    else:
        form = CreateGroupForm()

    return render(request, 'courses/create_group.html', {'form': form})


def group(request, group_id):
    group = Group.objects.get(id=group_id)
    return render(request, 'courses/group.html', {'group': group})


def create_event(request, group_id):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = Event.objects.create(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                is_required_to_pass_the_course=form.cleaned_data['is_required_to_pass_the_course'],
                min_tasks_positive=form.cleaned_data['min_tasks_positive'],
                weight=form.cleaned_data['weight'],
                group_id=group_id
            )
            tasks_count = form.cleaned_data['tasks_count']
            if tasks_count > 0:
                return HttpResponseRedirect(f'/courses/createTasks/{event.id}/{tasks_count}')
            else:
                return HttpResponseRedirect(f'/courses/group/{group_id}')
    else:
        form = CreateEventForm()

    return render(request, 'courses/create_event.html', {'form': form})


def create_event_tasks(request, event_id, tasks_count):
    TasksFormSet = formset_factory(CreateTaskForm, extra=tasks_count)

    if request.method == 'POST':
        formset = TasksFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                Task.objects.create(
                    event_id=event_id,
                    name=form.cleaned_data['name'],
                    max_points=form.cleaned_data['max_points']
                )
            return HttpResponseRedirect(f'/courses/group/{Event.objects.get(id=event_id).group.id}')
    else:
        formset = TasksFormSet()

    return render(request, 'courses/create_tasks.html', {'formset': formset})


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
