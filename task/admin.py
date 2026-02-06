from django.contrib import admin
from .models import Task, TaskSubmission, TaskImage


# ---------------------- INLINE FOR TASK IMAGES ----------------------
class TaskImageInline(admin.TabularInline):
    model = TaskImage
    extra = 0
    readonly_fields = ('image', 'created_at')
    can_delete = True
    show_change_link = True


# ---------------------- INLINE FOR TASK SUBMISSIONS ----------------------
class TaskSubmissionInline(admin.TabularInline):
    model = TaskSubmission
    extra = 0
    readonly_fields = ('submitted_by', 'submitted_at', 'notes', 'status', 'submission_date')
    show_change_link = True
    can_delete = False


# ---------------------- TASK ADMIN ----------------------
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'task_name', 'get_assigned_to',
        'status', 'task_frequency', 'created_at'
    )

    list_filter = ('status', 'assigned_to')   # JSONField ko hata diya
    search_fields = ('task_name', 'assigned_to__name')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 50
    filter_horizontal = ('assigned_to',)

    inlines = [TaskSubmissionInline]

    fieldsets = (
        ('Task Info', {
            'fields': ('task_name', 'description', 'task_frequency')
        }),
        ('Assignment Details', {
            'fields': ('assigned_to', 'status')
        }),
    )

    readonly_fields = ('created_at',)

    # Show ManyToMany employees
    def get_assigned_to(self, obj):
        return ", ".join(emp.name for emp in obj.assigned_to.all())
    get_assigned_to.short_description = "Assigned To"

    # Actions
    @admin.action(description="✅ Mark selected tasks as completed")
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f"{updated} task(s) marked as completed.")
    
    @admin.action(description="🚧 Mark selected tasks as in progress")
    def mark_in_progress(self, request, queryset):
        updated = queryset.update(status='in_progress')
        self.message_user(request, f"{updated} task(s) marked as in progress.")
    
    actions = ['mark_completed', 'mark_in_progress']



# ---------------------- TASK SUBMISSION ADMIN ----------------------
@admin.register(TaskSubmission)
class TaskSubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'task', 'submitted_by', 'submitted_at', 'status'
    )

    list_filter = ('status', 'submitted_at', 'task__status')
    search_fields = ('task__task_name', 'submitted_by__name')
    ordering = ('-submitted_at',)
    date_hierarchy = 'submitted_at'
    list_select_related = ('task', 'submitted_by')
    inlines = [TaskImageInline]
    list_per_page = 50

    readonly_fields = ('submitted_at',)

    @admin.action(description="✅ Verify selected submissions")
    def verify_submissions(self, request, queryset):
        updated = queryset.update(status='verified')
        self.message_user(request, f"{updated} submission(s) verified.")

    @admin.action(description="❌ Reject selected submissions")
    def reject_submissions(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f"{updated} submission(s) rejected.")

    actions = ['verify_submissions', 'reject_submissions']



# ---------------------- TASK IMAGE ADMIN ----------------------
@admin.register(TaskImage)
class TaskImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'submission', 'created_at', 'preview')
    readonly_fields = ('created_at', 'preview')
    search_fields = ('submission__task__task_name', 'submission__submitted_by__name')
    ordering = ('-created_at',)

    def preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='100' height='100' style='object-fit:cover;'/>"
        return "No image"

    preview.allow_tags = True
    preview.short_description = "Preview"
