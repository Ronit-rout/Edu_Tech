from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.courses.models import Course, Enrollment

def get_object_or_ok(klass, *args, **kwargs):
    # Safe fallback wrapper
    try:
        from django.shortcuts import get_object_or_404
        return get_object_or_404(klass, *args, **kwargs)
    except:
        return klass.objects.get(*args, **kwargs)

def courses_catalog(request):
    courses = Course.objects.all()
    internships = courses.filter(course_type='INTERNSHIP')
    trainings = courses.filter(course_type='TRAINING')
    
    enrolled_course_ids = []
    if request.user.is_authenticated:
        enrolled_course_ids = Enrollment.objects.filter(student=request.user).values_list('course_id', flat=True)
        
    context = {
        'internships': internships,
        'trainings': trainings,
        'enrolled_course_ids': enrolled_course_ids,
    }
    return render(request, 'courses/catalog.html', context)

def course_details(request, slug):
    course = get_object_or_ok(Course, slug=slug)
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        is_enrolled = enrollment is not None

    context = {
        'course': course,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }
    return render(request, 'courses/details.html', context)

@login_required
def checkout(request, slug):
    course = get_object_or_ok(Course, slug=slug)
    
    # Check if already enrolled
    existing = Enrollment.objects.filter(student=request.user, course=course).first()
    if existing and (existing.is_paid or course.course_type == 'INTERNSHIP'):
        messages.info(request, f"You are already enrolled in {course.title}.")
        if course.course_type == 'TRAINING':
            return redirect('training_dashboard')
        return redirect('internship_track')
        
    if request.method == 'POST':
        # Mock payment authorization simulation
        enrollment, created = Enrollment.objects.get_or_create(student=request.user, course=course)
        enrollment.is_paid = True
        enrollment.save()
        
        messages.success(request, f"Enrollment confirmed for {course.title}! Thank you for your payment.")
        if course.course_type == 'TRAINING':
            return redirect('training_dashboard')
        return redirect('onboarding')  # For internships
        
    context = {
        'course': course,
    }
    if course.course_type == 'TRAINING':
        return render(request, 'courses/training_checkout.html', context)
    return render(request, 'courses/checkout.html', context)
