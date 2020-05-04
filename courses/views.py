from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


# Create your views here.
from courses.models import Course


def index(request):
    all_courses = Course.objects.all()
    context = {'courses': all_courses}
    return render(request, 'courses/index.html', context)


def blank(request):
    return render(request, 'courses/blank.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/courses')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
