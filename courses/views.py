from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from courses.models import Course


def index(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses/index.html', context)


def blank(request):
    return render(request, 'courses/blank.html')
