"""HallOfFame URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # authentication
    path('register/', include('courses.urls')),
    path('login/', include('courses.urls')),

    # general viewing of details
    path('courses/', include('courses.urls')),  # list of courses
    path('courses/<int:course_id>', include('courses.urls')),  # list of groups in course with possibility to join (students only), view, search, create (teachers only)
    path('courses/<int:course_id>/<int:group_id>', include('courses.urls')),  # group details
    path('courses/<int:course_id>/<int:group_id>/<int:event_id>', include('courses.urls')),  # event details for group participants only
    path('courses/<int:course_id>/<int:group_id>/grades', include('courses.urls')),  # table of grades
    path('courses/<int:course_id>/<int:group_id>/events', include('courses.urls')),  # events divided for past and upcomming

    # marking (for teachers only)
    path('courses/<int:course_id>/<int:group_id>/<int:event_id>/addGrades', include('courses.urls')),  # adding grades for event

    # creating (for teachers only)
    path('courses/createCourse', include('courses.urls')),  # create course form
    path('courses/<int:course_id>/createGroup', include('courses.urls')),  # create group form
    path('courses/<int:course_id>/<int:group_id>/createEvent', include('courses.urls')),  # create event in group form

]
