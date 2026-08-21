from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.courses.models import Course, Enrollment, Document
from apps.learning.models import Module, Task, Submission, Feedback, Interview, Certificate
from django.utils import timezone
import random

def homepage(request):
    return render(request, 'learning/index.html')

def about_us(request):
    return render(request, 'learning/about_us.html')

@login_required
def dashboard(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    submissions = Submission.objects.filter(student=request.user).order_by('-submitted_at')[:5]
    certificates = Certificate.objects.filter(student=request.user)
    
    # Active training enrollment
    training_enrollment = enrollments.filter(course__course_type='TRAINING').first()
    
    # Active internship enrollment
    internship_enrollment = enrollments.filter(course__course_type='INTERNSHIP').first()
    
    context = {
        'enrollments': enrollments,
        'submissions': submissions,
        'certificates': certificates,
        'training_enrollment': training_enrollment,
        'internship_enrollment': internship_enrollment,
    }
    return render(request, 'learning/dashboard.html', context)

@login_required
def onboarding(request):
    return render(request, 'learning/internship_planning.html')

@login_required
def career_paths(request):
    return render(request, 'learning/career_paths.html')

@login_required
def internship_track(request):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='INTERNSHIP').first()
    if not enrollment:
        messages.info(request, "Please enroll in an internship first.")
        return redirect('courses_catalog')
        
    modules = Module.objects.filter(course=enrollment.course).order_by('order')
    context = {
        'enrollment': enrollment,
        'modules': modules,
    }
    return render(request, 'learning/my_internship_workspace.html', context)

@login_required
def course_player(request):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='INTERNSHIP').first()
    if not enrollment:
        return redirect('courses_catalog')
        
    modules = Module.objects.filter(course=enrollment.course).order_by('order')
    first_module = modules.first()
    task = None
    if first_module:
        task = Task.objects.filter(module=first_module).first()
        
    submission = None
    if task:
        submission, _ = Submission.objects.get_or_create(student=request.user, task=task)
        
    context = {
        'enrollment': enrollment,
        'modules': modules,
        'active_module': first_module,
        'active_task': task,
        'submission': submission,
    }
    return render(request, 'learning/internship_workspace.html', context)

@login_required
def submit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        submission, created = Submission.objects.get_or_create(student=request.user, task=task)
        submission.submission_text = request.POST.get('submission_text', '')
        submission.file_url = request.POST.get('file_url', 'main.js')
        submission.status = 'SUBMITTED'
        submission.save()
        
        # Trigger simulated review pipeline
        # Auto-create feedback for student task after a short time or directly
        evaluator = request.user  # Self-evaluator mock
        Feedback.objects.update_or_create(
            submission=submission,
            defaults={
                'evaluator': evaluator,
                'score': 85,
                'comments': 'Excellent structure and neat code presentation. Ensure state handlers are clean.',
                'strengths': 'CSS organization, Flexbox rules, component structure.',
                'improvements': 'Move state triggers into container component context.',
                'retry_available': True
            }
        )
        
        # Update submission status to PASSED to let them progress
        submission.status = 'PASSED'
        submission.save()
        
        # Update enrollment progress
        enrollment = Enrollment.objects.filter(student=request.user, course=task.module.course).first()
        if enrollment:
            enrollment.progress_percent = min(100, enrollment.progress_percent + 25)
            enrollment.save()
            
        messages.success(request, "Task submitted and evaluation completed successfully!")
        
        if task.module.course.course_type == 'TRAINING':
            return redirect('training_dashboard')
        return redirect('evaluation_center')
    return redirect('dashboard')

@login_required
def evaluation_center(request):
    submissions = Submission.objects.filter(student=request.user).order_by('-submitted_at')
    context = {
        'submissions': submissions,
    }
    return render(request, 'learning/evaluation_center.html', context)

@login_required
def skills_wallet(request):
    certificates = Certificate.objects.filter(student=request.user)
    documents = Document.objects.filter(user=request.user)
    context = {
        'certificates': certificates,
        'documents': documents,
    }
    return render(request, 'learning/skills_wallet.html', context)

@login_required
def training_dashboard(request):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='TRAINING').first()
    if not enrollment:
        messages.info(request, "Please enroll in a Professional Training program to access the training area.")
        return redirect('courses_catalog')
        
    modules = Module.objects.filter(course=enrollment.course).order_by('level', 'order')
    
    # Calculate unlocked modules
    # In training, Level 1 must be completed before Level 2 unlocks, etc.
    unlocked_level = enrollment.current_level
    
    context = {
        'enrollment': enrollment,
        'modules': modules,
        'unlocked_level': unlocked_level,
    }
    return render(request, 'learning/training_dashboard.html', context)

@login_required
def training_module(request, module_id):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='TRAINING').first()
    if not enrollment:
        return redirect('courses_catalog')
        
    module = get_object_or_404(Module, id=module_id)
    
    # Ensure they can access this level
    if module.level > enrollment.current_level:
        messages.warning(request, "This level is currently locked. Complete previous evaluations first.")
        return redirect('training_dashboard')
        
    task = Task.objects.filter(module=module).first()
    submission = None
    if task:
        submission = Submission.objects.filter(student=request.user, task=task).first()
        
    context = {
        'enrollment': enrollment,
        'module': module,
        'task': task,
        'submission': submission,
    }
    return render(request, 'learning/training_module.html', context)

@login_required
def training_interview(request):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='TRAINING').first()
    if not enrollment:
        return redirect('courses_catalog')
        
    # Get or create interview details
    interview, created = Interview.objects.get_or_create(
        student=request.user,
        course=enrollment.course,
        defaults={
            'status': 'ELIGIBLE',
            'scheduled_at': timezone.now() + timezone.timedelta(days=2),
        }
    )
    
    if request.method == 'POST':
        # Book/Schedule the interview
        action = request.POST.get('action')
        if action == 'book':
            interview.status = 'SCHEDULED'
            interview.save()
            messages.success(request, "Interview successfully booked!")
        elif action == 'complete':
            interview.status = 'COMPLETED'
            interview.result_ready_at = timezone.now() + timezone.timedelta(hours=4)
            interview.save()
            messages.success(request, "Technical Interview completed! Evaluation result expected in ~4-5 hours.")
            
    context = {
        'enrollment': enrollment,
        'interview': interview,
    }
    return render(request, 'learning/training_interview.html', context)

@login_required
def training_score(request):
    enrollment = Enrollment.objects.filter(student=request.user, course__course_type='TRAINING').first()
    if not enrollment:
        return redirect('courses_catalog')
        
    interview = Interview.objects.filter(student=request.user, course=enrollment.course).first()
    
    # Mocking passing/failing score state
    score = 87
    status = 'PASSED'
    
    # Parameter overriding to mock failed attempt if needed
    result_param = request.GET.get('result', 'passed')
    if result_param == 'failed':
        score = 45
        status = 'FAILED'
        
    if request.method == 'POST' and status == 'PASSED':
        # Issue certificate
        cred_id = f"RL-{random.randint(100000, 999999)}"
        Certificate.objects.get_or_create(
            student=request.user,
            course=enrollment.course,
            defaults={
                'score': score,
                'credential_id': cred_id
            }
        )
        # Create Document certificate link
        Document.objects.get_or_create(
            user=request.user,
            name=f"RageLabs Training Certificate - {enrollment.course.title}",
            defaults={
                'doc_type': 'CERTIFICATE',
                'file_url': 'javascript:alert("Viewing certificate PDF link")'
            }
        )
        messages.success(request, "Certificate added to your Skills Wallet!")
        return redirect('skills_wallet')
        
    context = {
        'enrollment': enrollment,
        'interview': interview,
        'score': score,
        'status': status,
    }
    return render(request, 'learning/training_score.html', context)
