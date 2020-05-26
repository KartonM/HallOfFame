import csv
import os
from datetime import datetime

from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from courses.forms import SignUpStudentForm, SignUpTeacherForm
from .filters import UserFilter

from courses.forms import CreateCourseForm, CreateGroupForm, CreateEventForm, CreateTaskForm
from courses.forms import SignUpStudentForm, SignUpTeacherForm, RegisterTaskPointsForm, PickStudentForm, FileUploadForm
from courses.models import Course, Teacher, Group, Event, Task, Student, Grade, TaskPoints, CourseParticipation
# Create your views here.


def is_valid_seacrchparam(param):
    return param != '' and param is not None


def filter(request):
    qs = Course.objects.all()
    teachers = Teacher.objects.all()
    name_contains_query = request.GET.get('name_contains')
    description_query = request.GET.get('description')
    view_count_min = request.GET.get('view_count_min')
    view_count_max = request.GET.get('view_count_max')
    tutor = request.GET.get('teacher')

    if is_valid_seacrchparam(name_contains_query):
        qs = qs.filter(name__icontains=name_contains_query)

    elif is_valid_seacrchparam(description_query):
        qs = qs.filter(description__icontains=description_query)

    elif is_valid_seacrchparam(tutor) and tutor != 'Choose...':
        logger.error(tutor)
        id = Teacher.objects.filter(user_id=tutor).values('user_id')[0]['user_id']
        print(tutor)
        qs = qs.filter(tutor_id=id)

    if is_valid_seacrchparam(view_count_min):
        qs = qs.filter(views__gte=view_count_min)

    if is_valid_seacrchparam(view_count_max):
        qs = qs.filter(views__lt=view_count_max)

    return qs


def index(request):
    qs = filter(request)
    context = {
        'courses': qs,
        'teachers': Teacher.objects.all()
    }
    return render(request, 'courses/index.html', context)


def blank(request):
    return render(request, 'courses/blank.html')


def create_course(request):
    if request.method == 'POST':
        form = CreateCourseForm(request.POST)
        if form.is_valid():
            course = Course.objects.create(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                tutor=Teacher.objects.first()  # TODO use id of logged in teacher instead
            )
            return HttpResponseRedirect(f'{course.id}')
    else:
        form = CreateCourseForm()

    return render(request, 'courses/add_course.html', {'form': form})


def course(request, course_id):
    course = Course.objects.get(id=course_id)
    return render(request, 'courses/course.html', {'course': course})


def create_group(request, course_id):
    if request.method == 'POST':
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            Group.objects.create(
                tag=form.cleaned_data['tag'],
                size=form.cleaned_data['size'],
                course_id=course_id,
                teacher=form.cleaned_data['teacher']
            )
            return HttpResponseRedirect(f'/courses/{course_id}')
    else:
        form = CreateGroupForm()

    return render(request, 'courses/create_group.html', {'form': form})


def group(request, group_id):
    group = Group.objects.get(id=group_id)
    students = [course_participation.student for course_participation in group.courseparticipation_set.all()]
    members_with_grades = [(student, student.calculate_current_final(group_id)) for student in students]
    return render(
        request,
        'courses/group.html',
        {'group': group, 'file_upload_form': FileUploadForm(), 'members': members_with_grades}
    )


def create_event(request, group_id):
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            event = Event.objects.create(
                name=form.cleaned_data['name'],
                date=form.cleaned_data['date'],
                is_required_to_pass_the_course=form.cleaned_data['is_required_to_pass_the_course'],
                min_tasks_positive=form.cleaned_data['min_tasks_positive'],
                weight=form.cleaned_data['weight'],
                group_id=group_id
            )
            tasks_count = form.cleaned_data['tasks_count']
            if tasks_count > 0:
                return HttpResponseRedirect(f'/courses/createTasks/{event.id}/{tasks_count}')
            else:
                return HttpResponseRedirect(f'/courses/group/{group_id}')
    else:
        form = CreateEventForm()

    return render(request, 'courses/create_event.html', {'form': form})


def create_event_tasks(request, event_id, tasks_count):
    TasksFormSet = formset_factory(CreateTaskForm, extra=tasks_count)

    if request.method == 'POST':
        formset = TasksFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                Task.objects.create(
                    event_id=event_id,
                    name=form.cleaned_data['name'],
                    max_points=form.cleaned_data['max_points']
                )
            return HttpResponseRedirect(f'/courses/group/{Event.objects.get(id=event_id).group.id}')
    else:
        formset = TasksFormSet()

    return render(request, 'courses/create_tasks.html', {'formset': formset})


def add_grades(request, event_id):
    event = Event.objects.get(id=event_id)
    tasks_count = Task.objects.filter(event=event).count()
    task_names = []
    TaskPointsFormSet = formset_factory(RegisterTaskPointsForm, extra=tasks_count)

    if request.method == 'POST':
        formset = TaskPointsFormSet(request.POST)
        form = PickStudentForm(request.POST)
        if formset.is_valid() and form.is_valid():
            grade = Grade.objects.create(
                event=event,
                student=form.cleaned_data['student'],
                date_of_registration=datetime.now()
            )
            tasks = Task.objects.filter(event=event)
            for (points_form, task) in zip(formset, tasks):
                TaskPoints.objects.create(
                    grade=grade,
                    task=task,
                    points=min(points_form.cleaned_data['points'], task.max_points)
                )
            return HttpResponseRedirect(f'/courses/group/{event.group.id}')
    else:
        formset = TaskPointsFormSet()
        group_students_ids = event.group.courseparticipation_set.values_list('student', flat=True)
        graded_students_ids = event.grade_set.values_list('student', flat=True)
        students_choice = Student.objects.filter(pk__in=group_students_ids).exclude(pk__in=graded_students_ids)
        form = PickStudentForm(students_choice_set=students_choice)
        task_names = Task.objects.filter(event=event).values_list('name', flat=True)

    return render(
        request,
        'courses/add_grades.html',
        {'points_formset': formset, 'student_form': form, 'task_names': task_names}
    )


def upload_grades(request, event_id):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = f'courses/tmp/{event_id}_{datetime.timestamp(datetime.now())}.csv'
            grades, errors = save_grades_file(request.FILES['file'], file_path, event_id)
            return render(
                request,
                'courses/uploaded_grades_preview.html',
                {
                    'grades': grades,
                    'errors': errors,
                    'task_names': Task.objects.filter(event_id=event_id).values_list('name', flat=True),
                    'event_id': event_id,
                    'csv_file_path': file_path
                }
            )

    return HttpResponseRedirect(f'/courses/group/{Event.objects.get(id=event_id).group_id}')


def save_grades_file(file, file_path, event_id):
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    return parse_grades_file(file_path, event_id)


def parse_grades_file(file_path, event_id):
    grades = []
    errors = []
    event = Event.objects.get(id=event_id)
    tasks = Task.objects.filter(event=event)
    with open(file_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) < len(tasks) + 1:
                errors.append(f'Following row doesn\'t have enough columns: {row}')
                continue
            student_name_or_card_id = row[0]
            student = Student.objects.filter(student_card_id=student_name_or_card_id).first()
            if student is None:
                students = Student.objects.filter(
                    user__first_name__in=student_name_or_card_id.split(),
                    user__last_name__in=student_name_or_card_id.split()
                )
                if students.count() > 1:
                    errors.append(f'Group has more than one student with name {row[0]}')
                student = students.first()

            if student is None:
                errors.append(f'No student for {row[0]} was found.')
                continue

            grade = Grade(event=event, student=student, date_of_registration=datetime.now())
            task_points = []

            for i, task in enumerate(tasks, start=1):
                points = int(row[i])
                if points > task.max_points:
                    errors.append(f'Max points for task {task} is {task.max_points} but given value was {points}')
                task_points.append(TaskPoints(grade=grade, task=task, points=min(points, task.max_points)))

            grades.append((grade, task_points))

    return grades, errors


def confirm_upload(request, event_id, csv_file_path):
    grades, errors = parse_grades_file(csv_file_path, event_id)
    tasks = Task.objects.filter(event_id=event_id)
    for grade, task_points_list in grades:
        grade.save()
        for task_points, task in zip(task_points_list, tasks):
            task_points.grade = grade
            task_points.task = task

        TaskPoints.objects.bulk_create(task_points_list)

    os.remove(csv_file_path)

    return HttpResponseRedirect(f'/courses/group/{Event.objects.get(id=event_id).group_id}')


def cancel_upload(request, event_id, csv_file_path):
    os.remove(csv_file_path)

    return HttpResponseRedirect(f'/courses/group/{Event.objects.get(id=event_id).group_id}')


def pick_register(request):
    return render(request, 'registration/pickRegister.html')


def signup_student(request):
    if request.method == 'POST':
        form = SignUpStudentForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(student_card_id=form.cleaned_data.get('index_no'), user=user)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/courses')
    else:
        form = SignUpStudentForm()
    return render(request=request,
                  template_name='registration/register.html',
                  context={'form': form})


def signup_teacher(request):
    if request.method == 'POST':
        form = SignUpTeacherForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            Teacher.objects.create(academic_degree=form.cleaned_data.get('academic_degree'), user=user)
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('/courses')
    else:
        form = SignUpTeacherForm()
    return render(request=request,
                  template_name='registration/register.html',
                  context={'form': form})


def join_group(request, pk, student):
    group_to_join = Group.objects.get(pk=pk)

    CourseParticipation.objects.create(
        group=group_to_join,
        student=student,
    )
    return redirect(request, 'home')


def search(request):
    course_list = User.objects.all()
    course_filter = UserFilter(request.GET, queryset=course_list)
    return render(request, 'courses/index.html', {'filter': course_filter})


def join(request, group_id):
    group = Group.objects.get(pk=group_id)

    if request.method == 'POST':
        CourseParticipation.objects.create(
            group=group,
            student=request.user.student,
        )
        return redirect('/group/' + str(group_id) )
    else:
        return render(request, '/courses/index.html')



@login_required
def upcoming_events(request):
    user = request.user
    events = []
    student = Student.objects.filter(user__username__exact=request.user.username).first()
    teacher = Teacher.objects.filter(user__username__exact=request.user.username).first()
    if student is not None:
        event_ids = user.student.courseparticipation_set.values_list('group__event', flat=True)
        events = Event.objects.filter(pk__in=event_ids).filter(date__gte=datetime.now()).order_by('-date')
    elif teacher is not None:
        event_ids = user.teacher.group_set.values_list('event', flat=True)
        events = Event.objects.filter(pk__in=event_ids).filter(date__gte=datetime.now()).order_by('-date')
    return render(request=request,
                  template_name='courses/upcoming_events.html',
                  context={'events': events})

