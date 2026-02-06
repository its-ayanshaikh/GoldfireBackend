from django.contrib import admin
from .models import Role, Employee, Attendance, Leave, Salary, LeaveSwapRequest, SalesCommission, PaidLeaveRequest, MonthlyLeaveRequest, MonthlyLeaveItem  # 👈 add LeaveSwapRequest

admin.site.register(SalesCommission)

# ---------------------- ROLE ADMIN ----------------------
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    search_fields = ('name',)
    ordering = ('name',)


# ---------------------- ATTENDANCE INLINE ----------------------
class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0
    readonly_fields = ('date', 'login_time', 'logout_time', 'status', 'total_hours', 'overtime_hours', 'break_hours')
    can_delete = False
    show_change_link = True


# ---------------------- LEAVE INLINE ----------------------
class LeaveInline(admin.TabularInline):
    model = Leave
    extra = 0
    readonly_fields = ('leave_date', 'notes')
    can_delete = False
    show_change_link = True


# ---------------------- EMPLOYEE ADMIN ----------------------
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'email', 'branch', 'role',
        'joining_date', 'base_salary'
    )
    list_filter = ('branch', 'role', 'joining_date')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)
    inlines = [AttendanceInline, LeaveInline]

    fieldsets = (
        ('Personal Info', {
            'fields': ('name', 'email', 'phone', 'address', 'emergency_contact')
        }),
        ('Job Details', {
            'fields': ('branch', 'role', 'joining_date')
        }),
        ('Salary Details', {
            'fields': ('base_salary', 'overtime_multiplier', 'working_hours', 'shift_in', 'shift_out')
        }),
    )

    readonly_fields = ('created_at',)


# ---------------------- ATTENDANCE ADMIN ----------------------
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'date', 'status', 'login_time', 'logout_time', 'total_hours', 'overtime_hours', 'break_hours')
    list_filter = ('status', 'date')
    search_fields = ('employee__name', 'employee__email')
    ordering = ('-date',)
    date_hierarchy = 'date'
    list_per_page = 50


# ---------------------- LEAVE ADMIN ----------------------
@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'leave_date', 'created_at')
    list_filter = ('leave_date',)
    search_fields = ('employee__name',)
    ordering = ('-leave_date',)
    actions = ['approve_leave', 'reject_leave']

    @admin.action(description="Approve selected leaves")
    def approve_leave(self, request, queryset):
        updated = queryset.update(status='approved')
        self.message_user(request, f"{updated} leave(s) approved.")

    @admin.action(description="Reject selected leaves")
    def reject_leave(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} leave(s) rejected.")


# ---------------------- PAID LEAVE ADMIN ----------------------
from django.contrib import admin
from .models import PaidLeaveRequest


@admin.register(PaidLeaveRequest)
class PaidLeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee',
        'leave_date',
        'replace_with_date',
        'status',
        'approved_by',
        'created_at',
    )

    list_filter = ('status', 'leave_date', 'replace_with_date', 'created_at')
    search_fields = ('employee__name', 'employee__email', 'leave_date', 'replace_with_date')
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at', 'approved_by')

    actions = ['approve_requests', 'reject_requests']

    @admin.action(description="Approve selected Paid Leave Requests")
    def approve_requests(self, request, queryset):
        count = 0
        for req in queryset.filter(status='pending'):
            req.status = 'approved'
            req.approved_by = request.user
            req.save()
            count += 1

        self.message_user(request, f"{count} paid leave request(s) approved.")

    @admin.action(description="Reject selected Paid Leave Requests")
    def reject_requests(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} paid leave request(s) rejected.")



# ---------------------- SALARY ADMIN ----------------------
@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'employee', 'month', 'year', 'base_salary', 'overtime_salary',
        'commission', 'deduction', 'gross_salary', 'status', 'paid_amount'
    )
    list_filter = ('year', 'month', 'status')
    search_fields = ('employee__name', 'employee__email')
    ordering = ('-year', '-month')
    readonly_fields = ('gross_salary', 'created_at')
    actions = ['mark_as_paid']

    @admin.action(description="Mark selected salaries as paid")
    def mark_as_paid(self, request, queryset):
        updated = queryset.update(status='paid')
        self.message_user(request, f"{updated} salary record(s) marked as paid.")


# ---------------------- LEAVE SWAP REQUEST ADMIN 🆕 ----------------------
@admin.register(LeaveSwapRequest)
class LeaveSwapRequestAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'from_employee',
        'to_employee',
        'from_leave',
        'to_leave',
        'status',
        'created_at',
        'updated_at',
    )
    list_filter = ('status', 'created_at')
    search_fields = (
        'from_employee__name',
        'to_employee__name',
        'from_leave__leave_date',
        'to_leave__leave_date',
    )
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_swap', 'reject_swap']

    @admin.action(description="Approve selected swap requests")
    def approve_swap(self, request, queryset):
        count = 0
        for swap in queryset.filter(status='pending'):
            # Swap the leave dates
            from_date = swap.from_leave.leave_date
            to_date = swap.to_leave.leave_date

            swap.from_leave.leave_date = to_date
            swap.to_leave.leave_date = from_date
            swap.from_leave.save()
            swap.to_leave.save()

            swap.status = 'approved'
            swap.save()
            count += 1

        self.message_user(request, f"{count} swap request(s) approved and processed.")

    @admin.action(description="Reject selected swap requests")
    def reject_swap(self, request, queryset):
        updated = queryset.filter(status='pending').update(status='rejected')
        self.message_user(request, f"{updated} swap request(s) rejected.")


# --------------------------
# INLINE: MonthlyLeaveItem
# --------------------------
class MonthlyLeaveItemInline(admin.TabularInline):
    model = MonthlyLeaveItem
    extra = 0
    readonly_fields = ('leave_date', 'status', 'approved_by', 'created_at')
    fields = ('leave_date', 'status', 'approved_by')
    can_delete = False
    show_change_link = False


# --------------------------
# ACTIONS for parent request
# --------------------------

def approve_all_items(modeladmin, request, queryset):
    count = 0
    for req in queryset:
        items = req.leaves.filter(status='pending')
        for item in items:
            item.approve(by_user=request.user)
            count += 1
    
    modeladmin.message_user(request, f"{count} leave items approved.")
approve_all_items.short_description = "Approve ALL pending leave items in selected requests"


def reject_all_items(modeladmin, request, queryset):
    count = 0
    for req in queryset:
        items = req.leaves.filter(status='pending')
        for item in items:
            item.reject(by_user=request.user)
            count += 1
    
    modeladmin.message_user(request, f"{count} leave items rejected.")
reject_all_items.short_description = "Reject ALL pending leave items in selected requests"


# --------------------------
# ADMIN: MonthlyLeaveRequest
# --------------------------
@admin.register(MonthlyLeaveRequest)
class MonthlyLeaveRequestAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'employee',
        'aggregate_status',
        'created_at',
    )

    list_filter = ('aggregate_status', 'created_at', 'employee__branch')
    search_fields = ('employee__name', 'employee__email')
    ordering = ('-created_at',)

    readonly_fields = ('created_at', 'updated_at', 'aggregate_status')

    inlines = [MonthlyLeaveItemInline]

    actions = [approve_all_items, reject_all_items]


# -----------------------------------
# ADMIN: MonthlyLeaveItem (Optional)
# -----------------------------------
@admin.register(MonthlyLeaveItem)
class MonthlyLeaveItemAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'request',
        'leave_date',
        'status',
        'approved_by',
        'created_at',
    )

    list_filter = ('status', 'leave_date', 'approved_by')
    search_fields = ('request__employee__name',)
    ordering = ('-leave_date',)

    readonly_fields = ('created_at', 'updated_at')