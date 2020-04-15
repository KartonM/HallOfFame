import os, django, random, string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "HallOfFame.settings")
django.setup()

from django.contrib.auth.models import User
from courses.models import Teacher, Student, Course, Group, CourseParticipation
from faker import Faker

STUDENTS_COUNT = 6
TEACHERS_COUNT = 4
COURSES_COUNT = 3

MIN_GROUPS_PER_COURSE = 1
MAX_GROUPS_PER_COURSE = 2

MIN_GROUP_SIZE = 10
MAX_GROUP_SIZE = 15

MIN_GROUP_FULFILLMENT = 0.2
MAX_GROUP_FULFILLMENT = 1

fake = Faker()


def generate_user():
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = (first_name + last_name).lower()
    email = f'{first_name[0]}.{last_name}@{fake.free_email_domain()}'
    return User.objects.create(username=username, email=email, password='qweqweqwe', first_name=first_name, last_name=last_name)


def generate_users(count):
    users = []
    for _ in range(count):
        users.append(generate_user())
    return users


def generate_teacher(user):
    degree = random.choice(['mgr', 'mgr inż.', 'dr', 'prof.', 'dr hab.'])
    return Teacher.objects.create(academic_degree=degree, user=user)


def generate_student(user):
    student_card_id = ''.join(random.choice(string.digits) for _ in range(6))
    return Student.objects.create(student_card_id=student_card_id, user=user)


def generate_course(tutor):
    name = fake.sentence()
    description = fake.paragraph()
    return Course.objects.create(name=name, description=description, tutor=tutor)


def generate_groups_for_course(course, teachers):
    groups = []
    week_days = ['pon', 'wt', 'sr', 'czw', 'pt']
    lesson_start_times = ['800', '935', '1115', '1250', '1440', '1615', '1750', '1920']
    groups_count = random.randint(MIN_GROUPS_PER_COURSE, MAX_GROUPS_PER_COURSE)
    for _ in range(groups_count):
        teacher = random.choice(teachers)
        groups.append(Group.objects.create(
            course=course,
            group_tag=random.choice(week_days) + random.choice(lesson_start_times),
            size=random.randint(MIN_GROUP_SIZE, MAX_GROUP_SIZE),
            teacher=teacher
        ))
    return groups


def generate_course_participation(group, students):
    course_participation_entries = []
    group_fulfillment = random.uniform(MIN_GROUP_FULFILLMENT, MAX_GROUP_FULFILLMENT)
    group_members_count = min(int(group.size * group_fulfillment), len(students))

    for student in random.sample(students, group_members_count):
        course_participation_entries.append(CourseParticipation.objects.create(
            student=student,
            group=group,
        ))
    return course_participation_entries


def chunks(list_, count):
    return (list_[i::count] for i in range(count))


def generate():
    users = generate_users(STUDENTS_COUNT + TEACHERS_COUNT)

    teachers = []
    students = []
    courses = []
    all_groups = []
    course_participation_entities = []

    for user in users[:STUDENTS_COUNT]:
        students.append(generate_student(user))

    for user in users[STUDENTS_COUNT:]:
        teachers.append(generate_teacher(user))

    for _ in range(COURSES_COUNT):
        tutor = random.choice(teachers)
        courses.append(generate_course(tutor))

    for course in courses:
        groups_for_course = generate_groups_for_course(course=course, teachers=teachers)
        all_groups += groups_for_course

        random.shuffle(students)
        group_students_pools = list(chunks(students, len(groups_for_course)))

        assert len(groups_for_course) == len(group_students_pools), f'groups_for_course and group_student_pools ' \
                                                                    f'should have equal length\n' \
                                                                    f'{groups_for_course}\n{group_students_pools}'

        for group, students in zip(groups_for_course, group_students_pools):
            course_participation_entities += generate_course_participation(group=group, students=students)

    print(users)
    print(students)
    print(teachers)
    print(courses)
    print(len(all_groups))
    print(all_groups)
    print(len(course_participation_entities))
    print(course_participation_entities)


generate()
