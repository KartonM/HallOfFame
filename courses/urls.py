from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('register/', views.blank, name='blank'),
    path('login/', views.blank, name='blank'),
    path('<int:course_id>', views.course, name='course'),
    path('<int:course_id>/<int:group_id>', views.blank, name='blank'),  # group details
    path('<int:course_id>/<int:group_id>/<int:event_id>', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/grades', views.blank, name='blank'),  # table of grades
    path('<int:course_id>/<int:group_id>/events', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/<int:event_id>/addGrades', views.blank, name='blank'),
    path('createCourse', views.create_course, name='create_course'),
    path('<int:course_id>/createGroup', views.create_group, name='create_group'),
    path('<int:course_id>/<int:group_id>/createEvent', views.blank, name='blank'),
    path('myGrades', views.blank, name='blank'),

]

