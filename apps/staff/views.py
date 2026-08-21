from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from apps.courses.models import Course, Enrollment, Document
from apps.learning.models import Submission, Feedback, Certificate
from apps.accounts.models import User

def is_staff_user(user):
    return user.is_authenticated and (user.role in ['ADMIN', 'EDUCATOR', 'HR'] or user.is_superuser)

def is_admin_user(user):
    return user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser)

def is_educator_user(user):
    return user.is_authenticated and (user.role == 'EDUCATOR' or user.is_superuser)

def is_hr_user(user):
    return user.is_authenticated and (user.role == 'HR' or user.is_superuser)

@user_passes_test(is_educator_user)
def educator_studio(request):
    courses = Course.objects.all()
    context = {
        'courses': courses,
    }
    return render(request, 'staff/educator_program_builder.html', context)

@user_passes_test(is_hr_user)
def hr_dashboard(request):
    students = User.objects.filter(role='STUDENT')
    context = {
        'students': students,
    }
    return render(request, 'staff/hr_talent_intelligence_dashboard.html', context)

@user_passes_test(is_admin_user)
def admin_overview(request):
    submissions_count = Submission.objects.count()
    certificates_count = Certificate.objects.count()
    students_count = User.objects.filter(role='STUDENT').count()
    
    recent_submissions = Submission.objects.order_by('-submitted_at')[:5]
    
    context = {
        'submissions_count': submissions_count,
        'certificates_count': certificates_count,
        'students_count': students_count,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'staff/admin_overview.html', context)

@user_passes_test(is_admin_user)
def admin_student_profile(request):
    # View student 360 profile
    student = User.objects.filter(role='STUDENT').first()
    enrollments = Enrollment.objects.filter(student=student) if student else []
    submissions = Submission.objects.filter(student=student) if student else []
    
    context = {
        'student': student,
        'enrollments': enrollments,
        'submissions': submissions,
    }
    return render(request, 'staff/admin_student_360_profile.html', context)

@user_passes_test(is_admin_user)
def admin_evaluation_center(request):
    submissions = Submission.objects.all().order_by('-submitted_at')
    context = {
        'submissions': submissions,
    }
    return render(request, 'staff/admin_evaluation_center.html', context)

@user_passes_test(is_admin_user)
def admin_health_monitor(request):
    return render(request, 'staff/admin_system_health_ai_monitor.html')
