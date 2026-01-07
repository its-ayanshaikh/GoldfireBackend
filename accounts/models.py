from django.contrib.auth.models import AbstractUser
from django.db import models
from company.models import Branch

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('subadmin', 'Sub Admin'),
        ('cashier', 'POS Cashier'),
        ('employee', 'Employee'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if self.branch:
            return f"{self.username} ({self.role}) - {self.branch.name}"
        return f"{self.username} ({self.role})"
