from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Task, TaskSubmission, TaskImage
from rest_framework.response import Response
from .pagination import TaskPagination
from django.utils.timezone import now
from employee.models import Employee
from .utils import compress_image
from rest_framework import status
from django.db.models import Q
from datetime import timedelta
from .serializers import *


# --------------------------
# CREATE TASK
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_task(request):
    try:
        data = request.data.copy()
        data['assigned_by'] = request.user.id
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# LIST TASKS
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_tasks(request):
    try:
        queryset = Task.objects.all().order_by('-id')

        # -----------------------
        # SEARCH (task_name)
        # -----------------------
        search = request.GET.get("search")
        if search:
            queryset = queryset.filter(task_name__icontains=search)

        # -----------------------
        # FILTER BY EMPLOYEE
        # -----------------------
        employee_id = request.GET.get("employee_id")
        if employee_id:
            queryset = queryset.filter(assigned_to__id=employee_id)

        # -----------------------
        # PAGINATION
        # -----------------------
        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(queryset, request)

        serializer = TaskSerializer(paginated_tasks, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=400)



# --------------------------
# GET TASK DETAILS
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=200)

    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# UPDATE TASK
# --------------------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# DELETE TASK
# --------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_task(request, pk):
    try:
        task = Task.objects.get(id=pk)
        task.delete()
        return Response({"message": "Task deleted"}, status=200)

    except Task.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# EPLOYEES TASK
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_today_tasks(request):
    try:
        # Logged in user → employee
        employee = request.user.employee_profile
        if not employee:
            return Response({"error": "Employee profile not found"}, status=404)

        # Calculate today's day (your format)
        import datetime
        from django.utils.timezone import localdate
        
        today = localdate()
        python_day = datetime.datetime.today().isoweekday()     # Mon=1 ... Sun=7
        your_day = python_day + 1                                # Convert to your format
        if your_day == 8:                                        # If 8 → make 1 (Sunday)
            your_day = 1

        # Filter tasks:
        # - employee assigned ho
        # - today's frequency ho
        tasks = Task.objects.filter(
            assigned_to=employee,
            task_frequency__days__contains=[your_day],
            submissions__submitted_by=employee,
            submissions__submission_date=today,
            submissions__status="pending"
        ).order_by('-id').distinct()

        # Response
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# SUBMIT TASK
# --------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_task(request):
    try:
        # Logged user → employee
        employee = request.user.employee_profile
        if not employee:
            return Response({"error": "Employee profile not found"}, status=404)

        # Task ID
        task_id = request.data.get("task")
        if not task_id:
            return Response({"error": "Task ID is required"}, status=400)

        # Fetch task
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=404)

        # IST time
        from django.utils.timezone import now, localdate
        from datetime import timedelta
        ist_time = now() + timedelta(hours=5, minutes=30)
    
        today = localdate()
        # GET OR CREATE (MAIN CHANGE)
        submission, created = TaskSubmission.objects.get_or_create(
            task=task,
            submitted_by=employee,
            submission_date=today,
            defaults={
                "notes": "",
                "submitted_at": ist_time,
                "status": "submitted"
            }
        )

        # Agar existing submission tha, to update karege
        if not created:
            submission.notes = request.data.get("notes", submission.notes)
            submission.submitted_at = ist_time
            submission.status = "submitted"
            submission.save()

        # Handle Images
        images = request.FILES.getlist("images")
        for img in images:
            compressed_img = compress_image(img)
            TaskImage.objects.create(submission=submission, image=compressed_img)

        # Response
        serializer = TaskSubmissionSerializer(submission)
        return Response(serializer.data, status=201)

    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=400)
    

# --------------------------
# GET SUBMITTED TASK BY EMPLOYEE
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def today_submitted_tasks(request):
    try:
        employee = request.user.employee_profile

        if not employee:
            return Response({"error": "Employee profile not found"}, status=404)

        import datetime
        python_day = datetime.datetime.today().isoweekday()
        your_day = python_day + 1
        if your_day == 8:
            your_day = 1

        submissions = TaskSubmission.objects.filter(
            submitted_by=employee,
            status="submitted",
            task__task_frequency__days__contains=[your_day]
        ).order_by('-id')

        serializer = TaskSubmissionSerializer(submissions, many=True)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# --------------------------
# ALL SUBMISSIONS
# --------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_all_submissions(request):
    try:
        submissions = TaskSubmission.objects.all().order_by('-id')

        # -----------------------------
        # Search by task name OR employee name
        # -----------------------------
        search = request.GET.get("search")
        if search:
            submissions = submissions.filter(
                Q(task__task_name__icontains=search) |
                Q(submitted_by__name__icontains=search)
            )

        # -----------------------------
        # Filter by date (submitted_at)
        # date=2025-01-20
        # -----------------------------
        date = request.GET.get("date")
        if date:
            submissions = submissions.filter(
                submitted_at__date=date
            )

        # -----------------------------
        # Filter by status
        # status=submitted / verified / rejected / pending
        # -----------------------------
        status_filter = request.GET.get("status")
        if status_filter:
            submissions = submissions.filter(status=status_filter)

        # -----------------------------
        # Pagination
        # -----------------------------
        paginator = TaskPagination()
        paginated_submissions = paginator.paginate_queryset(submissions, request)

        serializer = TaskSubmissionSerializer(paginated_submissions, many=True)
        return paginator.get_paginated_response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=400)
