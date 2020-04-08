from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.
from courses.models import Course


def index(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses/index.html', context)


def detail(request, course_id):
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        raise Http404("Course does not exist")
    return render(request, 'courses/courseDetails.html', {'course': course})


def detail1(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

