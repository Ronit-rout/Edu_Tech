"""
Database Seeding Script for RageLabs Learning Demo.
Run this script using `python seed.py` to set up all standard roles, courses, and modules.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'raise_labs.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.courses.models import Course, Enrollment
from apps.learning.models import Module, Task

User = get_user_model()

def seed_database():
    print("Seeding database...")

    # 1. Create Users
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={'email': 'admin@ragelabs.com', 'role': 'ADMIN', 'is_staff': True, 'is_superuser': True}
    )
    if not created:
        admin_user.email = 'admin@ragelabs.com'
        admin_user.save()
    if created or admin_user.check_password('ragelabs123') is False:
        admin_user.set_password('ragelabs123')
        admin_user.save()
        print("  Admin user created/updated.")

    educator_user, created = User.objects.get_or_create(
        username='educator',
        defaults={'email': 'educator@ragelabs.com', 'role': 'EDUCATOR'}
    )
    if not created:
        educator_user.email = 'educator@ragelabs.com'
        educator_user.save()
    if created or educator_user.check_password('ragelabs123') is False:
        educator_user.set_password('ragelabs123')
        educator_user.save()
        print("  Educator user created/updated.")

    hr_user, created = User.objects.get_or_create(
        username='hr',
        defaults={'email': 'hr@ragelabs.com', 'role': 'HR'}
    )
    if not created:
        hr_user.email = 'hr@ragelabs.com'
        hr_user.save()
    if created or hr_user.check_password('ragelabs123') is False:
        hr_user.set_password('ragelabs123')
        hr_user.save()
        print("  HR user created/updated.")

    student_user, created = User.objects.get_or_create(
        username='student',
        defaults={'email': 'student@ragelabs.com', 'role': 'STUDENT'}
    )
    if not created:
        student_user.email = 'student@ragelabs.com'
        student_user.save()
    if created or student_user.check_password('ragelabs123') is False:
        student_user.set_password('ragelabs123')
        student_user.save()
        print("  Student user created/updated.")

    # 2. Create Courses
    webarch_course, created = Course.objects.get_or_create(
        slug='webarch',
        defaults={
            'title': 'Modern Web Architect',
            'description': 'Master the design of scalable front-end systems, modular components, and responsive grid layouts.',
            'course_type': 'INTERNSHIP',
            'duration_weeks': 8,
            'difficulty': 'INTERMEDIATE',
        }
    )
    if created:
        print("  Course 'Modern Web Architect' created.")

    fullstack_course, created = Course.objects.get_or_create(
        slug='fullstack',
        defaults={
            'title': 'Full-Stack Development Training',
            'description': 'Our flagship professional training program covering HTML, CSS Grid, React, and backend API engineering.',
            'course_type': 'TRAINING',
            'price': 2500.00,
            'duration_weeks': 12,
            'difficulty': 'ADVANCED',
        }
    )
    if created:
        print("  Course 'Full-Stack Development Training' created.")

    # 3. Create Modules & Tasks
    # Modules for Web Architect (Internship)
    m1, _ = Module.objects.get_or_create(
        course=webarch_course,
        level=1,
        order=1,
        defaults={
            'title': 'React Component Design',
            'description': 'Examine composability patterns, component interfaces, and state encapsulation.',
            'content': '<p>Component styling principles and dynamic class builders.</p>'
        }
    )
    Task.objects.get_or_create(
        module=m1,
        order=1,
        defaults={
            'title': 'Build a Weather Component',
            'description': 'Create a modular react component fetching live APIs.',
            'requirements': 'Use React functional components\nSupport responsive breakpoints\nImplement error boundaries'
        }
    )

    # Modules for Full-Stack Development (Training)
    tm1, _ = Module.objects.get_or_create(
        course=fullstack_course,
        level=1,
        order=1,
        defaults={
            'title': 'Advanced Layouts: CSS Grid & Flexbox',
            'description': 'Design modern bento grids, vertical steppers, and layout structures.',
            'content': '<p>Master layout alignment rules and flex properties.</p>'
        }
    )
    Task.objects.get_or_create(
        module=tm1,
        order=1,
        defaults={
            'title': 'Bento Grid Portfolio',
            'description': 'Design a responsive personal portfolio using grid mechanics.',
            'requirements': 'Implement 3-column layout\nCollapsible sidebar\nZero overflow'
        }
    )

    tm2, _ = Module.objects.get_or_create(
        course=fullstack_course,
        level=2,
        order=1,
        defaults={
            'title': 'Advanced API Services',
            'description': 'Design RESTful API schemas and database mappings.',
            'content': '<p>Examine backend logic, ORM interactions, and data security.</p>'
        }
    )
    Task.objects.get_or_create(
        module=tm2,
        order=1,
        defaults={
            'title': 'Secure Authentication System',
            'description': 'Build session models and role verification middleware.',
            'requirements': 'Password encryption\nToken support\nRole-based gates'
        }
    )

    # 4. Enroll Student in Internship
    Enrollment.objects.get_or_create(
        student=student_user,
        course=webarch_course,
        defaults={
            'is_paid': True,
            'progress_percent': 25,
        }
    )
    print("  Student enrolled in Internship.")

    print("\nDatabase seeding completed successfully.")

if __name__ == '__main__':
    seed_database()
