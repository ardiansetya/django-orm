import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'simplelms.settings'
import django
django.setup()

import csv
from django.contrib.auth.models import User
from core.models import Course, CourseMember

# Import Users
with open('./dummy_data/user-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                username=row['username'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                email=row['email'],
                password=row['password']
            )

# Check if users were created successfully
print("Users created:")
for user in User.objects.all():
    print(f"{user.username} - {user.first_name} {user.last_name}")

# Import Courses
with open('./dummy_data/course-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        teacher_full_name = row['teacher']
        if not teacher_full_name:
            print(f"Skipping course '{row['name']}' due to missing teacher information.")
            continue  # Skip this row if teacher information is missing
            
        print(f"Trying to get teacher with full name: {teacher_full_name}")
        
        try:
            # Assuming you want to search by first and last name
            teacher = User.objects.get(first_name=teacher_full_name.split()[0], last_name=teacher_full_name.split()[1])
            if not Course.objects.filter(pk=num+1).exists():
                Course.objects.create(
                    id=num+1,
                    name=row['name'], 
                    description=row['description'], 
                    price=row['price'],
                    teacher=teacher
                )
        except User.DoesNotExist:
            print(f"Teacher with full name '{teacher_full_name}' does not exist.")
            
# Import Course Members
with open('./dummy_data/member-data.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not CourseMember.objects.filter(pk=num+1).exists():
            try:
                course = Course.objects.get(pk=int(row['course_id']))
                user = User.objects.get(username=row['user_id'])  # Adjusted to use username
                CourseMember.objects.create(
                    course=course,
                    user=user,
                    roles=row['roles']  # Ensure 'roles' is a field in your model
                )
            except Course.DoesNotExist:
                print(f"Course with ID '{row['course_id']}' does not exist.")
            except User.DoesNotExist:
                print(f"User with username '{row['user_id']}' does not exist.")
