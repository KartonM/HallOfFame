from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


# Create your models here.
GRADES = (
    ('2.0', '2.0'),
    ('3.0', '3.0'),
    ('3.5', '3.5'),
    ('4.0', '4.0'),
    ('4.5', '4.5'),
    ('5.0', '5.0'),
)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student_card_id = models.CharField(max_length=16)

    def __str__(self):
        return self.user.get_full_name()


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    academic_degree = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.academic_degree} {self.user.get_full_name()}'


class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def seats_count(self):
        return self.group_set.aggregate(Sum('size'))['size__sum']

    def __str__(self):
        return self.name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tag = models.CharField(max_length=15)
    size = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher}, {self.tag}'


class CourseParticipation(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    final_grade = models.CharField(max_length=3, choices=GRADES, null=True)

    def __str__(self):
        return f'{self.student} assigned to {self.group}'


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    is_required_to_pass_the_course = models.BooleanField()
    min_tasks_positive = models.PositiveSmallIntegerField(default=0)
    weight = models.PositiveSmallIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def max_points(self):
        return self.task_set.aggregate(Sum('max_points'))['max_points__sum']

    def __str__(self):
        return f'{self.name}, {self.date.date()}'


class Grade(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    value = models.CharField(max_length=3, choices=GRADES, null=True)
    date_of_registration = models.DateTimeField()

    def points(self):
        return self.taskpoints_set.aggregate(Sum('points'))['points__sum']

    def max_points(self):
        return self.presence.event.max_points()


class Task(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    max_points = models.PositiveSmallIntegerField()


class TaskPoints(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField()
