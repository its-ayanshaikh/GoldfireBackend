from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login, logout
from .models import User
from rest_framework.permissions import IsAuthenticated
from employee.models import PaidLeaveRequest, Leave
from django.utils import timezone
import pytz


def get_tokens_for_user(user):
    """
    Helper function to generate JWT tokens for user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Function-based JWT login API with optional Django session
    """
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'Please provide username and password.'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(request, username=username, password=password)

    if user is not None:
        # Generate JWT tokens
        tokens = get_tokens_for_user(user)

        # Optional: Create Django session (for admin or backend tracking)
        login(request, user)
        # ---------- Get today's Indian date ----------
        # ist = pytz.timezone('Asia/Kolkata')
        today = timezone.now().date()

        paid_leave_requested = False
        paid_leave_status = "none"
        is_on_leave_today = False  # NEW FIELD
        shift_in = None
        shift_out = None
        username=user.username

        # ---------- Check only if user is employee ----------
        if hasattr(user, 'employee_profile') and user.employee_profile:
            employee = user.employee_profile

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
            
            shift_in = employee.shift_in
            shift_out = employee.shift_out
            
            username = employee.name

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': username,
                'user_type': user.role,
                'branch': user.branch.name if user.branch else None,
                'paid_leave_requested': paid_leave_requested,
                'is_on_leave_today': is_on_leave_today,
                'paid_leave_status': paid_leave_status if paid_leave_requested else "none",
                'shift_in': shift_in,
                'shift_out': shift_out,
            },
            'tokens': tokens
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_user(request):
    """
    Function-based logout API - destroys session
    """
    logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    try:
        user = request.user

        # ---------- Get today's Indian date ----------
        # ist = pytz.timezone('Asia/Kolkata')
        today = timezone.now().date()

        paid_leave_requested = False
        paid_leave_status = "none"
        is_on_leave_today = False  # NEW FIELD

        # ---------- Check only if user is employee ----------
        if hasattr(user, 'employee_profile') and user.employee_profile:
            employee = user.employee_profile

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

        # ---------- Response ----------
        return Response({
            'id': user.id,
            'username': user.username,
            'user_type': user.role,
            'branch': user.branch.name if user.branch else None,

            'paid_leave_requested': paid_leave_requested,
            'paid_leave_status': paid_leave_status if paid_leave_requested else "none",

            'is_on_leave_today': is_on_leave_today,  # NEW FIELD
        })

    except Exception as e:

        return Response(
            {"error": "Something went wrong", "details": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
