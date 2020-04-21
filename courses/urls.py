from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.blank, name='blank'),
    path('login/', views.blank, name='blank'),
    path('<int:course_id>', views.course, name='course'),
    path('group/<int:group_id>', views.group, name='group'),  # group details
    path('<int:course_id>/<int:group_id>/<int:event_id>', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/grades', views.blank, name='blank'),  # table of grades
    path('<int:course_id>/<int:group_id>/events', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/<int:event_id>/addGrades', views.blank, name='blank'),
    path('createCourse', views.create_course, name='create_course'),
    path('<int:course_id>/createGroup', views.create_group, name='create_group'),
    path('group/<int:group_id>/createEvent', views.create_event, name='create_event'),
    path('createTasks/<int:event_id>/<int:tasks_count>', views.create_event_tasks, name='create_tasks'),
    path('myGrades', views.blank, name='blank'),

]

