from django.contrib.auth.models import User
from courses.models import Course
import django_filters


class UserFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    class Meta:
        model = Course
        fields = ['tutor', 'name', 'description', ]


