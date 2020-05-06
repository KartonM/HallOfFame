from django.urls import path
from . import views
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),

    path('accounts/signupStudent', views.signup_student, name='signup'),
    path('accounts/signupTeacher', views.signup_teacher, name='signup'),
    path('accounts/', views.pick_register, name='register_pick'),

    path('register/', views.blank, name='blank'),
    path('login/', views.blank, name='blank'),
    path('<int:course_id>', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>', views.blank, name='blank'),  # group details
    path('<int:course_id>/<int:group_id>/<int:event_id>', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/grades', views.blank, name='blank'),  # table of grades
    path('<int:course_id>/<int:group_id>/events', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/<int:event_id>/addGrades', views.blank, name='blank'),
    path('createCourse', views.blank, name='blank'),
    path('<int:course_id>/createGroup', views.blank, name='blank'),
    path('<int:course_id>/<int:group_id>/createEvent', views.blank, name='blank'),
    path('myGrades', views.blank, name='blank'),

]

