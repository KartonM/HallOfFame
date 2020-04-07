from django.contrib import admin

# Register your models here.
from courses.models import Course, Group


class GroupInline(admin.StackedInline):
    model = Group
    extra = 1


class CourseAdmin(admin.ModelAdmin):
    inlines = [GroupInline]


admin.site.register(Course, CourseAdmin)
