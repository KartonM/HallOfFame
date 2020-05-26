# Generated by Django 3.0.6 on 2020-05-25 15:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('is_required_to_pass_the_course', models.BooleanField()),
                ('min_tasks_positive', models.PositiveSmallIntegerField(default=0)),
                ('weight', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(choices=[('2.0', '2.0'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0')], max_length=3, null=True)),
                ('date_of_registration', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('student_card_id', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_points', models.PositiveSmallIntegerField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('academic_degree', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='TaskPoints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.PositiveSmallIntegerField()),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Grade')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Task')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=15)),
                ('size', models.PositiveSmallIntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='grade',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Student'),
        ),
        migrations.AddField(
            model_name='event',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Group'),
        ),
        migrations.CreateModel(
            name='CourseParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_grade', models.CharField(choices=[('2.0', '2.0'), ('3.0', '3.0'), ('3.5', '3.5'), ('4.0', '4.0'), ('4.5', '4.5'), ('5.0', '5.0')], max_length=3, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Group')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Student')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Teacher'),
        ),
    ]
