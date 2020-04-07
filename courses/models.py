from django.db import models

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = models.TextField(blank=True)
    def __str__(self):
        return self.course_name

class Group(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    group_tag = models.CharField(max_length=15)
    size = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.group_tag