from django.db import models
from django.db.models import Sum


# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = models.TextField(blank=True)

    def seats_count(self):
        return self.group_set.aggregate(Sum('size'))['size__sum']

    def __str__(self):
        return self.course_name


class Teacher(models.Model):
    name = models.CharField(max_length=25)
    room = models.CharField(max_length=15)
    consultation = models.CharField(max_length=45, null=True, blank=True)
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group_tag = models.CharField(max_length=15)
    size = models.PositiveSmallIntegerField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True,)

    def __str__(self):
        return self.group_tag

