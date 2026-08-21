from django.db import models
from django.conf import settings

class Course(models.Model):
    TYPE_CHOICES = (
        ('INTERNSHIP', 'Internship'),
        ('TRAINING', 'Training'),
    )
    DIFFICULTY_CHOICES = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=100)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='INTERNSHIP')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    duration_weeks = models.IntegerField(default=8)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='INTERMEDIATE')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    is_paid = models.BooleanField(default=False)
    current_level = models.IntegerField(default=1)  # Level 1, 2, 3
    progress_percent = models.IntegerField(default=0)
    date_enrolled = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"

class Document(models.Model):
    DOC_TYPE_CHOICES = (
        ('RESOURCE', 'Learning Resource'),
        ('SUBMISSION', 'Project Submission'),
        ('CERTIFICATE', 'Certificate'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='documents')
    name = models.CharField(max_length=255)
    file_url = models.CharField(max_length=500, blank=True)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='RESOURCE')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
