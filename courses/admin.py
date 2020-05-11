from django.contrib import admin

# Register your models here.
from courses.models import Course, Group, Teacher, Student, CourseParticipation, Grade, TaskPoints


class GroupInline(admin.StackedInline):
    model = Group
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [GroupInline]


admin.site.register(Course, CourseAdmin)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(CourseParticipation)
admin.site.register(Grade)
admin.site.register(TaskPoints)