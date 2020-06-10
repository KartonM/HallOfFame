import csv
from datetime import datetime
from courses.models import Event, Task, Student, Grade, TaskPoints


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
        csv_reader = csv.reader(csv_file, delimiter=';')
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
