from .serializers import MonthlyLeaveRequestSerializer, RoleSerializer, EmployeeSerializer, LeaveSerializer, LeaveSwapRequestSerializer, AttendanceSerializer, SalarySerializer, PaidLeaveRequestListSerializer, MonthlyLeaveCreateSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework import status
from .models import *
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.db.models import Q
from django.utils import timezone
import calendar
from dateutil.relativedelta import relativedelta 
from .utils import *

User = get_user_model()


# -------------------------------
# Create a new Role
# -------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_role(request):
    """
    Create a new role
    Example body: {"name": "Manager"}
    """
    try:
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------
# List all Roles
# -------------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_roles(request):
    """
    Get all roles
    """
    try:
        roles = Role.objects.all().order_by('id')
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------
# Edit / Update a Role
# -------------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_role(request, pk):
    """
    Update a role by ID
    Example body: {"name": "Updated Role Name"}
    """
    try:
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = RoleSerializer(role, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Role updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# -------------------------------
# Delete a Role
# -------------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_role(request, pk):
    """
    Delete a role by ID
    """
    try:
        try:
            role = Role.objects.get(pk=pk)
        except Role.DoesNotExist:
            return Response({"error": "Role not found"}, status=status.HTTP_404_NOT_FOUND)

        role.delete()
        return Response({"message": "Role deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------
# Create Employee
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_employee(request):
    """
    Create a new Employee along with a default User account.
    Username = phone number
    Password = phone number
    Role = employee
    """
    try:
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # Save employee first
            employee = serializer.save()

            # Validate phone number availability
            if not employee.phone:
                return Response(
                    {"error": "Phone number is required to create user credentials."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            username = employee.phone.strip()
            password = employee.phone.strip()

            # Check if user with same username already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {"error": f"User with phone {username} already exists."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Create default user with phone as username & password
            user = User.objects.create_user(
                username=username,
                password=password,
                role="employee",
                branch=employee.branch,
                email=employee.email or None
            )

            # Link the user <-> employee
            employee.user = user
            employee.save()

            return Response(
                {
                    "message": "Employee & linked user created successfully.",
                    "employee": serializer.data,
                    "user_credentials": {
                        "username": username,
                        "password": password,
                        "role": user.role,
                        "branch": user.branch.name if user.branch else None,
                    }
                },
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ----------------------------
# List Employees
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_employees(request):
    """
    Get all employees (with pagination + search + filters)
    """
    try:
        from .pagination import EmployeePagination

        employees = Employee.objects.select_related('branch', 'role').order_by('-created_at')

        # ---------------------------------
        # SEARCH (name OR phone)
        # ---------------------------------
        search = request.GET.get("search")
        if search:
            employees = employees.filter(
                Q(name__icontains=search) |
                Q(phone__icontains=search)
            )

        # ---------------------------------
        # FILTER BY BRANCH
        # /employees/?branch=3
        # ---------------------------------
        branch_id = request.GET.get("branch")
        if branch_id:
            employees = employees.filter(branch_id=branch_id)

        # ---------------------------------
        # FILTER BY ROLE
        # /employees/?role=2
        # ---------------------------------
        role_id = request.GET.get("role")
        if role_id:
            employees = employees.filter(role_id=role_id)

        # ---------------------------------
        # PAGINATION
        # ---------------------------------
        paginator = EmployeePagination()
        paginated_qs = paginator.paginate_queryset(employees, request)

        serializer = EmployeeSerializer(paginated_qs, many=True)
        return paginator.get_paginated_response(serializer.data)
    

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ----------------------------
# Update Employee
# ----------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_employee(request, pk):
    """
    Update an employee by ID
    """
    try:
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Employee updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ----------------------------
# Delete Employee
# ----------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_employee(request, pk):
    """
    Delete an employee by ID
    """
    try:
        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        
        credential = User.objects.get(username=employee.phone)
        
        if credential:
            credential.delete()

        employee.delete()
        return Response({"message": "Employee deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

 
# ----------------------------
# Create Leave
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_leave(request):
    """
    Create a new leave record.
    Prevents duplicate leave for the same employee on the same date.
    Example body:
    {
        "employee_id": 2,
        "leave_date": "2025-10-09",
        "notes": "Medical leave"
    }
    """
    try:
        employee_id = request.data.get("employee_id")
        leave_date = request.data.get("leave_date")

        # Validation: both fields required
        if not employee_id or not leave_date:
            return Response(
                {"error": "Both 'employee_id' and 'leave_date' are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if same employee already has leave for same date
        from .models import Leave
        if Leave.objects.filter(employee_id=employee_id, leave_date=leave_date).exists():
            return Response(
                {"error": "Leave already exists for this employee on this date."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # Proceed with normal creation
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Leave created successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# ----------------------------
# List Leaves (month-wise)
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_leaves(request):
    """
    Get all leaves for a specific month & year.
    Example: /api/leaves/?month=10&year=2025
    """
    try:
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            return Response(
                {"error": "Please provide 'month' and 'year' query parameters."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            month = int(month)
            year = int(year)
        except ValueError:
            return Response({"error": "Month and Year must be integers."}, status=status.HTTP_400_BAD_REQUEST)

        # Filter by month and year
        leaves = Leave.objects.select_related('employee').filter(
            leave_date__year=year, leave_date__month=month
        ).order_by('-leave_date')

        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------
# Update Leave
# ----------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_leave(request, pk):
    """
    Update a leave record by ID.
    Prevent assigning duplicate leave date for same employee.
    """
    try:
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({"error": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

        employee_id = request.data.get("employee_id") or leave.employee_id
        leave_date = request.data.get("leave_date") or str(leave.leave_date)

        # 🔸 Check duplicate (ignore current record itself)
        if Leave.objects.filter(
            employee_id=employee_id,
            leave_date=leave_date
        ).exclude(id=pk).exists():
            return Response(
                {"error": "Leave already exists for this employee on this date."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = LeaveSerializer(leave, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Leave updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ----------------------------
# Delete Leave
# ----------------------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_leave(request, pk):
    """
    Delete a leave record by ID.
    """
    try:
        try:
            leave = Leave.objects.get(pk=pk)
        except Leave.DoesNotExist:
            return Response({"error": "Leave not found"}, status=status.HTTP_404_NOT_FOUND)

        leave.delete()
        return Response({"message": "Leave deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ----------------------------
# List Leaves by Employees
# ----------------------------
from datetime import datetime, timedelta
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_leaves_by_month(request):
    """
    Returns all leaves for the logged-in employee filtered by month (and optional year)
    Example frontend request:
    GET /api/my-leaves/?month=10&year=2025
    """
    # Get month and year from query params
    month = request.query_params.get('month')
    year = request.query_params.get('year')

    # Validate month param
    if not month:
        return Response({"error": "Month parameter is required. Example: ?month=10"}, status=400)

    try:
        month = int(month)
        if year:
            year = int(year)
        else:
            year = datetime.now().year
    except ValueError:
        return Response({"error": "Month and year must be integers."}, status=400)

    # Get current employee from logged-in user
    employee = getattr(request.user, 'employee_profile', None)
    if not employee:
        return Response({"error": "No employee profile found for this user."}, status=404)

    # Filter leaves by month and year
    leaves = Leave.objects.filter(
        employee=employee,
        leave_date__month=month,
        leave_date__year=year
    ).order_by('-leave_date')

    serializer = LeaveSerializer(leaves, many=True)
    return Response(serializer.data)

# ----------------------------
# Branch Employee Leaves List
# ----------------------------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def branch_employees_leaves(request):
    """
    Fetch all employees and their leaves under the logged-in user's branch.
    JWT token must belong to a user who has a branch.
    """
    # Get month and year from query params
    month = request.query_params.get('month')
    year = request.query_params.get('year')
    
    try:
        month = int(month)
        if year:
            year = int(year)
        else:
            year = datetime.now().year
    except ValueError:
        return Response({"error": "Month and year must be integers."}, status=400)
    
    user = request.user
    employee_self = getattr(user, 'employee_profile', None)
    
    # Check branch
    if not user.branch:
        return Response({"error": "User is not assigned to any branch."}, status=400)

    branch = employee_self.branch
    # Fetch employees of this branch
    employees = Employee.objects.filter(branch=branch).exclude(id=employee_self.id if employee_self else None)

    # Build response data
    data = {
        "branch": branch.name,
        "employees": []
    }

    for emp in employees:
        leaves = Leave.objects.filter(employee=emp, leave_date__month=month, leave_date__year=year).order_by('-leave_date')
        leave_serializer = LeaveSerializer(leaves, many=True)

        data["employees"].append({
            "id": emp.id,
            "name": emp.name,
            "email": emp.email,
            "phone": emp.phone,
            "leaves": leave_serializer.data
        })

    return Response(data)


# ----------------------------
# Swap Leave Request
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_swap_request(request):
    user = request.user
    from_employee = getattr(user, 'employee_profile', None)
    if not from_employee:
        return Response({"error": "No employee profile found for this user."}, status=404)

    to_employee_id = request.data.get('to_employee_id')
    from_leave_id = request.data.get('from_leave_id')
    to_leave_id = request.data.get('to_leave_id')

    if not (to_employee_id and from_leave_id and to_leave_id):
        return Response({"error": "Missing required fields."}, status=400)

    # Create swap request
    swap = LeaveSwapRequest.objects.create(
        from_employee=from_employee,
        to_employee_id=to_employee_id,
        from_leave_id=from_leave_id,
        to_leave_id=to_leave_id,
    )
    serializer = LeaveSwapRequestSerializer(swap)
    return Response(serializer.data, status=201)

# ----------------------------
# Respond Swap Leave Request
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def respond_swap_request(request, swap_id):
    user = request.user
    to_employee = getattr(user, 'employee_profile', None)
    if not to_employee:
        return Response({"error": "No employee profile found for this user."}, status=404)

    action = request.data.get('response')  # "approve" or "reject"
    try:
        swap = LeaveSwapRequest.objects.get(id=swap_id, to_employee=to_employee)
    except LeaveSwapRequest.DoesNotExist:
        return Response({"error": "Swap request not found or not authorized."}, status=404)

    if swap.status != 'pending':
        return Response({"error": "This request has already been processed."}, status=400)

    if action == 'approved':
        # Swap leave dates
        from_leave_date = swap.from_leave.leave_date
        to_leave_date = swap.to_leave.leave_date

        swap.from_leave.leave_date = to_leave_date
        swap.to_leave.leave_date = from_leave_date

        swap.from_leave.save()
        swap.to_leave.save()

        swap.status = 'approved'
        swap.save()

        return Response({"message": "Leave swap approved successfully."})
    elif action == 'rejected':
        swap.status = 'rejected'
        swap.save()
        return Response({"message": "Leave swap rejected."})
    else:
        return Response({"error": "Invalid action."}, status=400)

# ----------------------------
# Sent Swap Request
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_sent_swaps(request):
    """
    Returns all swap requests sent by logged-in employee filtered by month/year.
    """
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        return Response({"error": "No employee profile found for this user."}, status=404)

    # Get query params
    month = request.query_params.get('month')
    year = request.query_params.get('year')
    if not month:
        return Response({"error": "Month parameter is required. Example: ?month=10"}, status=400)
    
    try:
        month = int(month)
        year = int(year) if year else datetime.now().year
    except ValueError:
        return Response({"error": "Month and year must be integers."}, status=400)

    swaps = LeaveSwapRequest.objects.filter(
        from_employee=employee,
        created_at__month=month,
        created_at__year=year
    ).order_by('-created_at')

    serializer = LeaveSwapRequestSerializer(swaps, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_paid_leave_request(request):
    try:
        # 1. Check employee exist
        if not hasattr(request.user, 'employee_profile'):
            return Response(
                {"error": "Employee profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = request.user.employee_profile

        # 2. Required + Optional fields
        leave_date = request.data.get("leave_date")
        swap_with = request.data.get("swap_with")
        reason = request.data.get("reason")

        # 3. Validate mandatory leave_date
        if not leave_date:
            return Response(
                {"error": "leave_date is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 4. Process replace_with_date
        replace_with_date = None

        # If swap_with is provided → fetch that leave date
        if swap_with:
            try:
                leave_obj = Leave.objects.get(id=swap_with)
                replace_with_date = leave_obj.leave_date
            except Leave.DoesNotExist:
                return Response(
                    {"error": "Invalid swap_with leave ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # No swap → replace_with_date same as leave_date
            replace_with_date = leave_date

        # 5. Create PaidLeaveRequest
        paid_req = PaidLeaveRequest.objects.create(
            employee=employee,
            leave_date=leave_date,
            replace_with_date=replace_with_date,
            reason=reason,
            status="pending"
        )

        return Response(
            {
                "message": "Paid leave request created successfully.",
                "data": {
                    "id": paid_req.id,
                    "leave_date": paid_req.leave_date,
                    "replace_with_date": paid_req.replace_with_date,
                    "reason": paid_req.reason,
                    "status": paid_req.status,
                }
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        return Response(
            {
                "error": "Something went wrong.",
                "details": str(e)
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
# ----------------------------
# Get Paid Leave Requests (with filters)
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_paid_leave_requests(request):
    try:
        user = request.user

        # -------------------------------------
        # Base Query – depends on user role
        # -------------------------------------
        if user.role in ["admin", "subadmin"]:
            queryset = PaidLeaveRequest.objects.select_related(
                'employee', 'approved_by'
            ).order_by('-created_at')

        elif user.role == "employee":
            if not hasattr(user, "employee_profile"):
                return Response(
                    {"error": "Employee profile not found."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            queryset = PaidLeaveRequest.objects.filter(
                employee=user.employee_profile
            ).select_related(
                'employee', 'approved_by'
            ).order_by('-created_at')

        else:
            return Response(
                {"error": "You do not have permission to view these records."},
                status=status.HTTP_403_FORBIDDEN
            )

        # -------------------------------------
        # Apply Optional Filters
        # -------------------------------------
        date_param = request.query_params.get('date')
        name_param = request.query_params.get('name')

        # --- Filter by Date ---
        if date_param:
            queryset = queryset.filter(leave_date=date_param)

        # --- Search by Employee Name ---
        if name_param:
            queryset = queryset.filter(
                employee__name__icontains=name_param
            )

        # -------------------------------------
        # Serialize & Return
        # -------------------------------------
        serializer = PaidLeaveRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:

        return Response(
            {"error": "Something went wrong.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

# ----------------------------
# Update Paid Leave Request Status
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_paid_leave_status(request, request_id):
    try:
        new_status = request.data.get("status")
        if new_status not in ["approved", "rejected"]:
            return Response(
                {"error": "Invalid status. Use 'approved' or 'rejected'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch paid leave request
        try:
            leave_request = PaidLeaveRequest.objects.get(id=request_id)
        except PaidLeaveRequest.DoesNotExist:
            return Response({"error": "Paid leave request not found."},
                            status=status.HTTP_404_NOT_FOUND)

        employee = leave_request.employee
        leave_date = leave_request.leave_date
        swap_date = leave_request.replace_with_date  # swap_with date

        # ---------------------------
        # REJECT
        # ---------------------------
        if new_status == "rejected":
            leave_request.status = "rejected"
            leave_request.approved_by = request.user
            leave_request.save()

            return Response({"message": "Request rejected successfully."},
                            status=status.HTTP_200_OK)

        # ---------------------------
        # APPROVE
        # ---------------------------
        if new_status == "approved":
            leave_request.status = "approved"
            leave_request.approved_by = request.user
            leave_request.save()

            # If swap date is provided → update existing Leave entry
            if swap_date:
                try:
                    leave_obj = Leave.objects.get(
                        employee=employee,
                        leave_date=swap_date
                    )

                    # Swap → replace old date with new leave_date
                    leave_obj.leave_date = leave_date
                    leave_obj.save()

                except Leave.DoesNotExist:
                    return Response(
                        {"error": "Swap leave entry not found for employee."},
                        status=status.HTTP_404_NOT_FOUND
                    )

            return Response(
                {"message": "Paid leave request approved.",
                 "swap_updated": True if swap_date else False},
                status=status.HTTP_200_OK
            )

    except Exception as e:
        return Response(
            {"error": "Something went wrong.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        

# ----------------------------
# Get Leave Status
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_leave_status(request):
    try:
        user = request.user
        employee = getattr(user, 'employee_profile', None)
        
        if not employee:
            return Response({"error": "No employee profile found for this user."}, status=404)
        
        # ist = pytz.timezone('Asia/Kolkata')
        today = timezone.now().date()

        paid_leave_requested = False
        paid_leave_status = "none"
        is_on_leave_today = False  # NEW FIELD
        
         # ---------------------------
        # Check Paid Leave Request (Today)
        # ---------------------------
        leave_req = PaidLeaveRequest.objects.filter(
            employee=employee,
            leave_date=today
        ).first()

        if leave_req:
            paid_leave_requested = True
            paid_leave_status = leave_req.status   # pending / approved / rejected

        # ---------------------------
        # Check actual Leave table (Today)
        # ---------------------------
        is_on_leave_today = Leave.objects.filter(
            employee=employee,
            leave_date=today
        ).exists()
        
        return Response({
            "paid_leave_requested": paid_leave_requested,
            "paid_leave_status": paid_leave_status,
            "is_on_leave_today": is_on_leave_today
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ----------------------------
# Create Monthly Leaves
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_monthly_leaves(request):
    try:
        user = request.user

        # Ensure user is an employee
        if not hasattr(user, "employee_profile"):
            return Response(
                {"error": "Employee profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = user.employee_profile

        # Validate incoming payload
        serializer = MonthlyLeaveCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        leave_dates = serializer.validated_data["leave_dates"]

        # Remove duplicate dates inside payload
        if len(set(leave_dates)) != len(leave_dates):
            return Response(
                {"error": "Duplicate leave dates are not allowed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Current month & year
        today = timezone.now().date()
        month = today.month
        year = today.year

        # GET or CREATE parent request for this month
        parent_request, created = MonthlyLeaveRequest.objects.get_or_create(
            employee=employee,
            created_at__year=year,
            created_at__month=month
        )

        # Check if some dates already exist inside this month’s request
        existing = MonthlyLeaveItem.objects.filter(
            request=parent_request,
            leave_date__in=leave_dates
        ).values_list("leave_date", flat=True)

        if existing:
            return Response(
                {
                    "error": "Some dates already requested in this month.",
                    "existing_dates": [str(d) for d in existing]
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        created_items = []

        # CREATE child items
        for d in sorted(leave_dates):
            item = MonthlyLeaveItem.objects.create(
                request=parent_request,
                leave_date=d
            )
            created_items.append(str(item.leave_date))

        # Update aggregate status
        parent_request.recalc_aggregate_status()

        return Response(
            {
                "message": "Leave dates added successfully.",
                "request_id": parent_request.id,
                "employee": employee.name,
                "created_new_request": created,
                "added_leaves": created_items
            },
            status=status.HTTP_201_CREATED
        )

    except Exception as e:

        return Response(
            {"error": "Something went wrong.", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        
        
# ----------------------------
# List Monthly Leaves By Employee
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_leave_request_list(request):
    try:
        user = request.user

        # employee mil gaya
        if not hasattr(user, "employee_profile"):
            return Response(
                {"error": "Employee profile not found."},
                status=status.HTTP_400_BAD_REQUEST
            )

        employee = user.employee_profile

        # current month + 1 month
        today = timezone.now().date()
        current_month = today.strftime("%Y-%m")

        # filter: only next-month requests
        requests_qs = MonthlyLeaveRequest.objects.filter(
            employee=employee,
            created_at__startswith=current_month  # easy filter
        ).order_by('-created_at')

        serializer = MonthlyLeaveRequestSerializer(requests_qs, many=True)

        return Response({"data": serializer.data})

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# ----------------------------
# List Monthly Leaves By Admin
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def monthly_leave_request_list_admin(request):
    try:
        # Query Params
        month = request.query_params.get("month")
        year = request.query_params.get("year")
        branch_id = request.query_params.get("branch_id")
        employee_name = request.query_params.get("employee_name")

        # Defaults → Current month & year
        today = timezone.now().date()
        if not month:
            month = today.month
        if not year:
            year = today.year

        month = int(month)
        year = int(year)

        # Base filter by leave_date
        qs = MonthlyLeaveRequest.objects.filter(
            created_at__year=year,
            created_at__month=month
        ).distinct()

        # Filter by branch
        if branch_id:
            qs = qs.filter(employee__branch_id=branch_id)

        # Filter by employee name
        if employee_name:
            qs = qs.filter(employee__name__icontains=employee_name)

        # Order latest first
        qs = qs.order_by('-created_at')

        serializer = MonthlyLeaveRequestSerializer(qs, many=True)
        return Response({"data": serializer.data})

    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ----------------------------
# Update Monthly Leave Status
# ----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_monthly_leave_item_status(request, leave_id):
    try:
        user = request.user

        # Must be an approver (Admin/Manager) – optional role check
        # if not user.is_staff:
        #     return Response({"error": "Not allowed"}, status=403)

        # Validate status
        new_status = request.data.get("status")
        if new_status not in ["approved", "rejected"]:
            return Response(
                {"error": "Invalid status. Must be 'approved' or 'rejected'."},
                status=400
            )

        # Fetch item
        try:
            item = MonthlyLeaveItem.objects.get(id=leave_id)
        except MonthlyLeaveItem.DoesNotExist:
            return Response({"error": "Leave item not found."}, status=404)

        # If already approved/rejected → cannot update again (optional rule)
        if item.status in ["approved", "rejected"]:
            return Response(
                {"error": f"Already {item.status}. Cannot change again."},
                status=400
            )

        # Apply status
        if new_status == "approved":
            item.approve(by_user=user)
        else:
            item.reject(by_user=user)

        item.save()

        return Response(
            {
                "message": "Leave status updated successfully.",
                "item_id": item.id,
                "employee": item.request.employee.name,
                "new_status": item.status,
                "approved_by": user.id,
                "leave_date": item.leave_date,
                "aggregate_status": item.request.aggregate_status
            }
        )

    except Exception as e:

        return Response({"error": "Something went wrong", "details": str(e)}, status=500)

# ----------------------------
# Recieved Swap Request
# ----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_received_swaps(request):
    """
    Returns all swap requests received by logged-in employee filtered by month/year.
    """
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        return Response({"error": "No employee profile found for this user."}, status=404)

    # Get query params
    month = request.query_params.get('month')
    year = request.query_params.get('year')
    if not month:
        return Response({"error": "Month parameter is required. Example: ?month=10"}, status=400)
    
    try:
        month = int(month)
        year = int(year) if year else datetime.now().year
    except ValueError:
        return Response({"error": "Month and year must be integers."}, status=400)

    swaps = LeaveSwapRequest.objects.filter(
        to_employee=employee,
        created_at__month=month,
        created_at__year=year
    ).order_by('-created_at')

    serializer = LeaveSwapRequestSerializer(swaps, many=True)
    return Response(serializer.data)

# -----------------------------
# Employee Login API
# -----------------------------
from django.utils import timezone
# import pytz
# ist = pytz.timezone('Asia/Kolkata')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_login(request):
    try:
        user = request.user
        employee = getattr(user, 'employee_profile', None)
        if not employee:
            return Response({"error": "No employee profile found"}, status=404)
        
        branch = employee.branch
        
        # Frontend lat/long
        try:
            user_lat = Decimal(request.data.get('latitude'))
            user_long = Decimal(request.data.get('longitude'))
        except (TypeError, ValueError):
            return Response(
                {"error": "Latitude and longitude are required"},
                status=400
            )
        print("user lat: " , user_lat)
        print("user long: " , user_long)
        print("branch lat: ", branch.latitude)
        print("branch long: ", branch.longitude)

        # Calculate distance
        distance = calculate_distance(
            float(user_lat),
            float(user_long),
            float(branch.latitude),
            float(branch.longitude)
        )

        # 20 meter validation
        if distance > 50:
            return Response(
                {
                    "error": "You are away from your store. Please go inside the store.",
                    "distance_in_meters": round(distance, 2)
                },
                status=403
            )


        today = timezone.now().date()
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={'status': 'present'}
        )

        # Update login
        attendance.login_time = timezone.now()
        if 'login_image' in request.FILES:
            attendance.login_image = request.FILES['login_image']
        attendance.status = 'present'
        attendance.save()

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data)

    except Exception as e:
        return Response({"error": str(e)}, status=500) 

# -----------------------------
# Employee Logout API
# -----------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def attendance_logout(request):
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        return Response({"error": "No employee profile found"}, status=404)
    
    branch = employee.branch
    
     # Frontend lat/long
    try:
        user_lat = Decimal(request.data.get('latitude'))
        user_long = Decimal(request.data.get('longitude'))
    except (TypeError, ValueError):
        return Response(
            {"error": "Latitude and longitude are required"},
            status=400
        )

    # Calculate distance
    distance = calculate_distance(
        float(user_lat),
        float(user_long),
        float(branch.latitude),
        float(branch.longitude)
    )

    # 20 meter validation
    if distance > 50:
        return Response(
            {
                "error": "You are away from your store. Please go inside the store.",
                "distance_in_meters": round(distance, 2)
            },
            status=403
        )

    today = timezone.now().date()
    try:
        attendance = Attendance.objects.get(employee=employee, date=today)
    except Attendance.DoesNotExist:
        return Response({"error": "No login record found"}, status=400)

    attendance.logout_time = timezone.now()
    if 'logout_image' in request.FILES:
        attendance.logout_image = request.FILES['logout_image']

    # -----------------------------
    # Calculate total working hours
    # -----------------------------
    if attendance.login_time:
        total_seconds = (attendance.logout_time - attendance.login_time).total_seconds()
        total_hours = round(total_seconds / 3600, 2)
        attendance.total_hours = total_hours

        # Break hours
        break_hours = attendance.break_hours or Decimal(0)
        effective_hours = Decimal(max(total_hours - float(break_hours), 0))

        # Working & overtime
        working_hours = Decimal(employee.working_hours or 8)
        overtime_hours = max(effective_hours - working_hours, Decimal(0))
        attendance.overtime_hours = overtime_hours

        # -----------------------------
        # Salary Components
        # -----------------------------
        # attendance.date se month aur year nikal lo
        year = attendance.date.year
        month = attendance.date.month

        # is month ke total days
        days_in_month = calendar.monthrange(year, month)[1]

        # Salary calculation
        monthly_salary = Decimal(employee.base_salary)
        daily_salary = monthly_salary / Decimal(days_in_month) # Full day salary
        hourly_rate = daily_salary / working_hours

        # Deduction for missing hours
        missing_hours = max(working_hours - effective_hours, Decimal(0))
        deduction_amount = hourly_rate * missing_hours

        # Overtime earnings
        overtime_earning = hourly_rate * employee.overtime_multiplier * overtime_hours

        # -----------------------------
        # Update/Insert Salary Record
        # -----------------------------
        month = today.month
        year = today.year
        salary_obj, created = Salary.objects.get_or_create(
            employee=employee, month=month, year=year,
            defaults={
                'base_salary': Decimal(0),
                'overtime_salary': Decimal(0),
                'commission': Decimal(0),
                'deduction': Decimal(0),
                'status': 'pending'
            }
        )

        # Always add full daily salary (not hourly)
        salary_obj.base_salary += daily_salary

        # Add overtime and deduction
        salary_obj.overtime_salary += overtime_earning
        salary_obj.deduction += deduction_amount
        salary_obj.save()

    attendance.save()
    serializer = AttendanceSerializer(attendance)
    return Response(serializer.data)


# -----------------------------
# My Attendance Current Month
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_attendance(request):
    user = request.user
    employee = getattr(user, 'employee_profile', None)
    if not employee:
        return Response({"error": "No employee profile found"}, status=404)

    now = timezone.now()
    current_year = now.year
    current_month = now.month
    today = now.day

    start_date = datetime(current_year, current_month, 1).date()
    end_date = now.date()

    attendances_qs = Attendance.objects.filter(employee=employee, date__range=(start_date, end_date))
    attendance_map = {att.date: att for att in attendances_qs}

    data = []
    for day in range(1, today + 1):
        date_iter = datetime(current_year, current_month, day).date()
        if date_iter in attendance_map:
            att = attendance_map[date_iter]
            serializer = AttendanceSerializer(att)
            data.append(serializer.data)
        else:
            data.append({
                "id": None,
                "employee": employee.id,
                "login_time": None,
                "logout_time": None,
                "login_image": None,
                "logout_image": None,
                "status": "absent",
                "date": date_iter,
                "total_hours": None
            })

    return Response({
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "branch": employee.branch.name if employee.branch else None
        },
        "month": current_month,
        "year": current_year,
        "attendance": data
    })

    
# -----------------------------
# Employees Attendance Current Month
# -----------------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def emp_attendance(request, emp_id):
    employee = Employee.objects.filter(id=emp_id).first()
    if not employee:
        return Response({"error": "No employee profile found"}, status=404)

    now = timezone.now()

    # -----------------------------
    # Get month & year from query params (or default current)
    # -----------------------------
    month = request.query_params.get('month')
    year = request.query_params.get('year')

    try:
        month = int(month) if month else now.month
        year = int(year) if year else now.year
    except ValueError:
        return Response({"error": "Invalid month or year"}, status=400)

    # -----------------------------
    # Determine date range
    # -----------------------------
    # Start of month
    start_date = datetime(year, month, 1).date()

    # End date — either last day of that month OR today (if current month)
    if month == now.month and year == now.year:
        end_date = now.date()
    else:
        # Last day of month calculation
        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        end_date = (next_month - timezone.timedelta(days=1)).date()

    # -----------------------------
    # Fetch attendance records
    # -----------------------------
    attendances_qs = Attendance.objects.filter(
        employee=employee,
        date__range=(start_date, end_date)
    ).order_by('date')

    attendance_map = {att.date: att for att in attendances_qs}
    total_days = (end_date - start_date).days + 1

    # -----------------------------
    # Build response day by day
    # -----------------------------
    data = []
    for i in range(total_days):
        date_iter = start_date + timezone.timedelta(days=i)
        if date_iter in attendance_map:
            att = attendance_map[date_iter]
            serializer = AttendanceSerializer(att)
            data.append(serializer.data)
        else:
            data.append({
                "id": None,
                "employee": employee.id,
                "login_time": None,
                "logout_time": None,
                "login_image": None,
                "logout_image": None,
                "status": "absent",
                "date": date_iter,
                "total_hours": None,
                "overtime_hours": None
            })

    # -----------------------------
    # Return structured response
    # -----------------------------
    return Response({
        "employee": {
            "id": employee.id,
            "name": employee.name,
            "branch": employee.branch.name if employee.branch else None
        },
        "month": month,
        "year": year,
        "attendance": data
    })
    

    
# -----------------------------
# GET SALARY DETAILS
# -----------------------------   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_attendance(request):
    try:
        from django.utils import timezone
        from datetime import datetime
        from decimal import Decimal

        employee_id = request.data.get("employee_id")
        date = request.data.get("date")
        login_time_str = request.data.get("login_time")
        logout_time_str = request.data.get("logout_time")
        break_minutes = request.data.get("break_minutes", 0)

        # Validate employee
        try:
            employee = Employee.objects.get(id=employee_id)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)

        if not date:
            return Response({"error": "Date is required"}, status=400)

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=date_obj,
            defaults={"status": "present"}
        )

        # -------------------------------
        # 1️⃣ GET OLD VALUES BEFORE UPDATE
        # -------------------------------
        old_total = attendance.total_hours or Decimal(0)
        old_ot = attendance.overtime_hours or Decimal(0)
        old_break = attendance.break_hours or Decimal(0)

        # ---- LOGIN TIME ----
        if login_time_str:
            dt = datetime.strptime(login_time_str, "%Y-%m-%d %H:%M:%S")
            attendance.login_time = timezone.make_aware(dt)

        # ---- LOGOUT TIME ----
        if logout_time_str:
            dt = datetime.strptime(logout_time_str, "%Y-%m-%d %H:%M:%S")
            attendance.logout_time = timezone.make_aware(dt)

        # Break hours always applied AFTER login/logout check
        break_hours = Decimal(int(break_minutes) / 60)
        attendance.break_hours = break_hours
        attendance.save()

        # -----------------------------------------------------
        # Only when BOTH login + logout exist → salary logic runs
        # -----------------------------------------------------
        if attendance.login_time and attendance.logout_time:

            # -------------------------------
            # 2️⃣ CALCULATE NEW HOURS
            # -------------------------------
            login_dt = attendance.login_time
            logout_dt = attendance.logout_time

            # FIX MIDNIGHT CROSS-OVER (logout next day)
            if logout_dt < login_dt:
                logout_dt = logout_dt + timedelta(days=1)
                attendance.logout_time = logout_dt  # update new logout with next-day

            # Total time difference
            total_seconds = (logout_dt - login_dt).total_seconds()
            total_hours = Decimal(total_seconds / 3600)

            effective_hours = total_hours - break_hours
            effective_hours = max(effective_hours, Decimal(0))

            new_total = round(effective_hours, 2)
            working_hours = Decimal(employee.working_hours)

            if effective_hours > working_hours:
                new_ot = effective_hours - working_hours
            else:
                new_ot = Decimal(0)

            new_ot = round(new_ot, 2)

            # -------------------------------
            # 3️⃣ MONTHLY SALARY CALCULATION
            # -------------------------------
            attendance_month = attendance.date.month
            attendance_year = attendance.date.year

            # attendance.date se month aur year nikal lo
            year = attendance.date.year
            month = attendance.date.month

            # is month ke total days
            days_in_month = calendar.monthrange(year, month)[1]

            # Salary calculation
            monthly_salary = Decimal(employee.base_salary)
            daily_salary = monthly_salary / Decimal(days_in_month)
            hourly_rate = daily_salary / working_hours

            # OLD salary contribution
            old_eh = old_total - old_break
            old_eh = max(old_eh, Decimal(0))
            old_missing_hours = max(working_hours - old_eh, Decimal(0))
            old_deduction = hourly_rate * old_missing_hours
            old_ot_money = hourly_rate * Decimal(employee.overtime_multiplier) * old_ot

            # NEW salary contribution
            effective_hours = new_total - attendance.break_hours
            effective_hours = max(effective_hours, Decimal(0))
            new_missing_hours = max(working_hours - effective_hours, Decimal(0))
            new_deduction = hourly_rate * new_missing_hours
            new_ot_money = hourly_rate * Decimal(employee.overtime_multiplier) * new_ot

            # -------------------------------
            # 4️⃣ FETCH MONTHLY SALARY OBJECT
            # -------------------------------
            salary_obj, created = Salary.objects.get_or_create(
                employee=employee,
                month=attendance_month,
                year=attendance_year,
                defaults={
                    'base_salary': Decimal(0),
                    'overtime_salary': Decimal(0),
                    'commission': Decimal(0),
                    'deduction': Decimal(0),
                    'status': 'pending'
                }
            )

            # -------------------------------
            # 5️⃣ REMOVE OLD CONTRIBUTION
            # -------------------------------
            if old_total > 0 or old_ot > 0:
                salary_obj.base_salary -= daily_salary
                salary_obj.overtime_salary -= old_ot_money
                salary_obj.deduction -= old_deduction

            # -------------------------------
            # 6️⃣ ADD NEW CONTRIBUTION
            # -------------------------------
            salary_obj.base_salary += daily_salary
            salary_obj.overtime_salary += new_ot_money
            salary_obj.deduction += new_deduction

            salary_obj.save()

            # -------------------------------
            # 7️⃣ SAVE NEW ATTENDANCE VALUES
            # -------------------------------
            attendance.total_hours = total_hours
            attendance.overtime_hours = new_ot
            attendance.status = "present"

        # Now save attendance FINAL
        
        attendance.save()

        serializer = AttendanceSerializer(attendance)
        return Response(serializer.data, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=400)


# -----------------------------
# GET SALARY DETAILS
# -----------------------------   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_salaries(request):
    month = request.query_params.get('month')
    year = request.query_params.get('year')

    if not month or not year:
        return Response({"error": "Please provide both 'month' and 'year' parameters"}, status=400)

    salaries = Salary.objects.filter(month=month, year=year).select_related('employee')
    serializer = SalarySerializer(salaries, many=True)
    return Response(serializer.data)


# -----------------------------
# UPDATE SALARY PAYMENT
# -----------------------------   
@api_view(['POST'])
def update_salary_payment(request):
    try:
        salary_id = request.data.get("salary_id")
        paid_amount = request.data.get("paid_amount")
        status_val = request.data.get("status", 'paid')

        # Validate salary ID
        if not salary_id:
            return Response({"message": "salary_id is required"}, status=400)

        # Fetch salary record
        try:
            salary = Salary.objects.get(id=salary_id)
        except Salary.DoesNotExist:
            return Response({"message": "Salary not found"}, status=404)

        # Update allowed fields
        try:
            if paid_amount is not None:
                salary.paid_amount = paid_amount

            if status_val:
                salary.status = status_val

            # Set Indian Time for paid_at
            indian_time = timezone.now().date()
            salary.paid_at = indian_time

            salary.save()

        except Exception as e:
            return Response({"message": "Failed to update salary", "error": str(e)}, status=500)

        # Serialize and return updated salary
        try:
            serializer = SalarySerializer(salary)
            return Response({
                "message": "Salary updated successfully",
                "salary": serializer.data
            })
        except Exception as e:
            return Response({"message": "Failed to serialize salary", "error": str(e)}, status=500)

    except Exception as e:
        return Response({"message": "Something went wrong", "error": str(e)}, status=500)
