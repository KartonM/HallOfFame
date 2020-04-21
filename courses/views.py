from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from courses.models import Course, Teacher, Group
from courses.forms import CreateCourseForm, CreateGroupForm


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
                tutor=Teacher.objects.first()
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
            group = Group.objects.create(
                group_tag=form.cleaned_data['tag'],
                size=form.cleaned_data['size'],
                course_id=course_id,
                teacher=form.cleaned_data['teacher']
            )
            return HttpResponseRedirect(f'/courses/{course_id}')
    else:
        form = CreateGroupForm()

    return render(request, 'courses/create_group.html', {'form': form})
