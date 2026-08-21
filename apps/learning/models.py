from django.db import models
from django.conf import settings
from apps.courses.models import Course

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    level = models.IntegerField(default=1)  # Level 1, Level 2, Level 3
    order = models.IntegerField(default=1)
    content = models.TextField(blank=True)
    video_url = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.course.title} - L{self.level} M{self.order}: {self.title}"

class Task(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    order = models.IntegerField(default=1)
    is_project = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.module.title} - Task {self.order}: {self.title}"

class Submission(models.Model):
    STATUS_CHOICES = (
        ('NOT_STARTED', 'Not Started'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('PASSED', 'Passed'),
        ('NEEDS_IMPROVEMENT', 'Needs Improvement'),
        ('FAILED', 'Failed'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    submission_text = models.TextField(blank=True)
    file_url = models.CharField(max_length=500, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NOT_STARTED')
    submitted_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'task')

    def __str__(self):
        return f"{self.student.username} - {self.task.title} ({self.status})"

class Feedback(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='feedback')
    evaluator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='evaluations')
    score = models.IntegerField(default=0)
    comments = models.TextField()
    strengths = models.TextField(blank=True)
    improvements = models.TextField(blank=True)
    retry_available = models.BooleanField(default=True)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.submission.student.username} - {self.submission.task.title}"

class Interview(models.Model):
    STATUS_CHOICES = (
        ('ELIGIBLE', 'Eligible'),
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('AWAITING_RESULT', 'Awaiting Result'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='interviews')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='interviews')
    scheduled_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ELIGIBLE')
    final_score = models.IntegerField(null=True, blank=True)
    result_ready_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"Interview: {self.student.username} - {self.course.title}"

class Certificate(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    score = models.IntegerField(default=0)
    credential_id = models.CharField(max_length=100, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"Certificate: {self.student.username} - {self.course.title}"
