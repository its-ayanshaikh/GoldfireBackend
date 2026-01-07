from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
from company.models import Branch

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='employee_profile', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='employees')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=15, blank=True, null=True)
    joining_date = models.DateField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    shift_in = models.TimeField(help_text="Shift start time (24-hour format)", null=True, blank=True)
    shift_out = models.TimeField(help_text="Shift end time (24-hour format)", null=True, blank=True)
    overtime_multiplier = models.DecimalField(max_digits=4, decimal_places=2, default=1)
    working_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8)
    status = models.CharField(max_length=20, choices=[('active', 'Active'), ('terminated', 'Terminated'), ('on_leave', 'On Leave')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    login_time = models.DateTimeField(blank=True, null=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    login_image = models.ImageField(upload_to='attendance/login/', blank=True, null=True)
    logout_image = models.ImageField(upload_to='attendance/logout/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    date = models.DateField()
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    break_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default=0)
    total_hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    # ----------------------------
    # Compress images before save
    # ----------------------------
    def save(self, *args, **kwargs):
        # Compress login image
        if self.login_image and not str(self.login_image).startswith("attendance/login/"):
            compressed_image = self.compress_image(self.login_image)
            self.login_image.save(self.login_image.name, compressed_image, save=False)

        # ----------------------------
        # Compress logout image safely
        # ----------------------------
        if self.logout_image and not str(self.logout_image).startswith("attendance/logout/"):
            compressed_image = self.compress_image(self.logout_image)
            self.logout_image.save(self.logout_image.name, compressed_image, save=False)

        super().save(*args, **kwargs)

    def compress_image(self, uploaded_image):
        """
        Compress uploaded image to reduce file size.
        """
        image_temporary = Image.open(uploaded_image)
        output_io_stream = BytesIO()
        # Convert to RGB if PNG (to avoid transparency issues)
        if image_temporary.mode in ("RGBA", "P"):
            image_temporary = image_temporary.convert("RGB")
        # Save image with reduced quality
        image_temporary.save(output_io_stream, format='JPEG', quality=50)  # Adjust quality 50-80
        output_io_stream.seek(0)
        return ContentFile(output_io_stream.read(), name=uploaded_image.name)



class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leaves')
    leave_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.name} - {self.leave_date}"
    

class PaidLeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='paid_leave_requests'
    )

    # Aaj jis date pe leave chahiye
    leave_date = models.DateField()

    # Jis date ko replace/adjust karega (future OR past)
    replace_with_date = models.DateField(null=True, blank=True)

    reason = models.TextField(blank=True, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    approved_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_paid_leave_requests'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Same employee cannot submit multiple requests for same date pair
            models.UniqueConstraint(
                fields=['employee', 'leave_date'],
                name='unique_employee_paid_leave_request'
            )
        ]

    def __str__(self):
        return f"{self.employee.name} - Leave: {self.leave_date} → Replace: {self.replace_with_date} ({self.status})"

    
class LeaveSwapRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    from_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='swap_requests_sent')
    to_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='swap_requests_received')

    from_leave = models.ForeignKey(Leave, on_delete=models.CASCADE, related_name='swap_from_leave')
    to_leave = models.ForeignKey(Leave, on_delete=models.CASCADE, related_name='swap_to_leave')

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.from_employee.name} ↔ {self.to_employee.name} ({self.status})"
    
class MonthlyLeaveRequest(models.Model):
    employee = models.ForeignKey(
        'Employee',
        on_delete=models.CASCADE,
        related_name='monthly_leave_requests'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # optional cached aggregate status (not required, but handy)
    AGG_STATUS_CHOICES = [
        ('pending', 'Pending'),            # all items pending
        ('partial_approved', 'Partial Approved'), # mix of statuses
        ('approved', 'Approved'),          # all items approved
        ('rejected', 'Rejected'),          # all items rejected
    ]
    aggregate_status = models.CharField(max_length=20, choices=AGG_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Request #{self.id} - {self.employee.name}"

    def recalc_aggregate_status(self):
        """
        Recalculate aggregate_status from child items.
        Call this after any item status change.
        """
        items = self.leaves.all()
        if not items.exists():
            self.aggregate_status = 'pending'
            self.save(update_fields=['aggregate_status'])
            return

        statuses = set(items.values_list('status', flat=True))
        if statuses == {'approved'}:
            agg = 'approved'
        elif statuses == {'rejected'}:
            agg = 'rejected'
        elif statuses == {'pending'}:
            agg = 'pending'
        else:
            agg = 'partial_approved'  # mix
        self.aggregate_status = agg
        self.save(update_fields=['aggregate_status'])


class MonthlyLeaveItem(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    request = models.ForeignKey(
        MonthlyLeaveRequest,
        on_delete=models.CASCADE,
        related_name='leaves'
    )
    leave_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    approved_by = models.ForeignKey(
        'accounts.User',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_monthly_leave_items'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['request', 'leave_date'],
                name='unique_leave_date_per_request'
            )
        ]
        ordering = ['leave_date']

    def __str__(self):
        return f"{self.request.employee.name} - {self.leave_date} ({self.status})"

    def approve(self, by_user):
        self.status = 'approved'
        self.approved_by = by_user
        self.save(update_fields=['status', 'approved_by', 'updated_at'])

        # AUTO-CREATE Leave entry
        Leave.objects.get_or_create(
            employee=self.request.employee,
            leave_date=self.leave_date
        )

        # Update Parent Request Status
        self.request.recalc_aggregate_status()

    def reject(self, by_user=None):
        self.status = 'rejected'
        if by_user:
            self.approved_by = by_user
        self.save(update_fields=['status', 'approved_by', 'updated_at'])
        self.request.recalc_aggregate_status()
    

class SalesCommission(models.Model):
    salesperson = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # format: 'YYYY-MM'
    total_sales = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_commission = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('salesperson', 'month')


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    month = models.PositiveSmallIntegerField()  # 1-12
    year = models.PositiveSmallIntegerField()
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    overtime_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    status = models.CharField(max_length=15, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateField(null=True, blank=True)
    
    @property
    def gross_salary(self):
        return self.base_salary + self.overtime_salary + self.commission - self.deduction

    def __str__(self):
        return f"{self.employee.name} - {self.month}/{self.year}"
    
    class Meta:
        unique_together = ('employee', 'month', 'year')