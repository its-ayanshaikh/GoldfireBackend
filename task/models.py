from django.db import models
from employee.models import Employee
from django.db.models import JSONField 

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    task_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    assigned_to = models.ManyToManyField(Employee, related_name='assigned_tasks')
    assigned_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    task_frequency = JSONField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task_name


class TaskSubmission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='submissions')
    submitted_by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    submission_date = models.DateField(null=True, blank=True)  # New field for submission date
    submitted_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('submitted', 'Submitted'), ('verified', 'Verified'), ('rejected', 'Rejected')], default='pending')

    def __str__(self):
        return f"{self.task.task_name} - {self.submitted_by.name}"


class TaskImage(models.Model):
    submission = models.ForeignKey(TaskSubmission, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='task_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.submission}"
