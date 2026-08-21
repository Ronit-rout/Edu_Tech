from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.accounts.forms import StudentSignUpForm, ProfileForm
from apps.courses.models import Enrollment, Document

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome to RageLabs Learning.")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = StudentSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin():
                    return redirect('admin_overview')
                elif user.is_educator():
                    return redirect('educator_studio')
                elif user.is_hr():
                    return redirect('hr_dashboard')
                else:
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('homepage')

@login_required
def profile_view(request):
    profile = request.user.profile
    enrollments = Enrollment.objects.filter(student=request.user)
    documents = Document.objects.filter(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        else:
            messages.error(request, "Failed to update profile.")
    else:
        form = ProfileForm(instance=profile)
        
    context = {
        'form': form,
        'profile': profile,
        'enrollments': enrollments,
        'documents': documents,
        'stats': {
            'enrollments_count': enrollments.count(),
            'certificates_count': request.user.certificates.count(),
            'submissions_count': request.user.submissions.count(),
        }
    }
    return render(request, 'accounts/profile.html', context)
