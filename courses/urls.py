from django.urls import path
from . import views
from django.conf.urls import url

app_name = "HallOfFame"

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.search, name='index'),

    path('accounts/signupStudent', views.signup_student, name='signup'),
    path('accounts/signupTeacher', views.signup_teacher, name='signup'),
    path('accounts/', views.pick_register, name='register_pick'),

    path('<int:course_id>', views.course, name='course'),
    path('group/<int:group_id>', views.group, name='group'),  # group details
    path('<int:course_id>/<int:group_id>/<int:event_id>', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/grades', views.blank, name='blank'),  # table of grades
    path('<int:course_id>/<int:group_id>/events', views.blank, name='blank'),
    path('addGrades/<int:event_id>', views.add_grades, name='add_grades'),
    path('createCourse', views.create_course, name='create_course'),
    path('<int:course_id>/createGroup', views.create_group, name='create_group'),
    path('group/<int:group_id>/createEvent', views.create_event, name='create_event'),
    path('createTasks/<int:event_id>/<int:tasks_count>', views.create_event_tasks, name='create_tasks'),
    path('myGrades', views.blank, name='blank'),
    path('group/<int:group_id>/join', views.join, name='join'),

    path('uploadGrades/<int:event_id>', views.upload_grades, name='upload_grades'),
    path('confirmUpload/<int:event_id>/<path:csv_file_path>', views.confirm_upload, name='confirm_upload'),
    path('cancelUpload/<int:event_id>/<path:csv_file_path>', views.cancel_upload, name='cancel_upload'),
    path('myUpcomingEvents/', views.upcoming_events, name='upcoming_events'),
    path('myGrades/', views.grades, name='grades'),
]

