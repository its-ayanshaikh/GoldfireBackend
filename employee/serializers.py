from rest_framework import serializers
from .models import Employee, Branch, Role, Leave, LeaveSwapRequest, Attendance, Salary, PaidLeaveRequest, MonthlyLeaveRequest, MonthlyLeaveItem


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['id', 'name']

from django.contrib.auth.hashers import make_password

class EmployeeUpdateSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), source='branch', write_only=True, required=False
    )
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True, required=False
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'branch', 'branch_id', 'role', 'role_id',
            'name', 'email', 'phone', 'address', 'emergency_contact',
            'joining_date', 'base_salary', 'overtime_multiplier',
            'working_hours', 'status', 'created_at',
            'shift_in', 'shift_out'
        ]

    def update(self, instance, validated_data):
        """
        Employee + linked User update
        """

        user = instance.user  # FK User

        # ---------- PHONE CHANGE ----------
        new_phone = validated_data.get('phone', None)

        if new_phone and user:
            # username = phone
            user.username = new_phone

            # password = phone (hashed)
            user.password = make_password(new_phone)

        # ---------- USER FIELDS ----------
        if 'email' in validated_data and user:
            user.email = validated_data.get('email')

        if 'branch_id' in validated_data and user:
            branch_id = validated_data.get('branch_id')
            user.branch = Branch.objects.get(id=branch_id.id) if branch_id else None

        if 'role' in validated_data and user:
            user.role = validated_data.get('role').name  # agar Role model use ho raha ho

        if user:
            user.save()

        # ---------- EMPLOYEE UPDATE ----------
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class EmployeeSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    role = RoleSerializer(read_only=True)
    branch_id = serializers.PrimaryKeyRelatedField(
        queryset=Branch.objects.all(), source='branch', write_only=True
    )
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'branch', 'branch_id', 'role', 'role_id',
            'name', 'email', 'phone', 'address', 'emergency_contact',
            'joining_date', 'base_salary', 'overtime_multiplier',
            'working_hours', 'status', 'created_at', 'shift_in', 'shift_out'
        ]

class EmployeeMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'name']


class LeaveSerializer(serializers.ModelSerializer):
    employee = EmployeeMiniSerializer(read_only=True)
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='employee', write_only=True
    )

    class Meta:
        model = Leave
        fields = ['id', 'employee', 'employee_id', 'leave_date', 'notes', 'created_at']
        
class LeaveSwapRequestSerializer(serializers.ModelSerializer):
    from_employee_name = serializers.CharField(source='from_employee.name', read_only=True)
    to_employee_name = serializers.CharField(source='to_employee.name', read_only=True)
    from_leave_date = serializers.DateField(source='from_leave.leave_date', read_only=True)
    to_leave_date = serializers.DateField(source='to_leave.leave_date', read_only=True)

    class Meta:
        model = LeaveSwapRequest
        fields = [
            'id',
            'from_employee', 'to_employee',
            'from_leave', 'to_leave',
            'from_employee_name', 'to_employee_name',
            'from_leave_date', 'to_leave_date',
            'status', 'created_at', 'updated_at'
        ]
        
class PaidLeaveRequestListSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    employee_branch = serializers.CharField(source='employee.branch', read_only=True)
    approved_by_name = serializers.CharField(source='approved_by.username', read_only=True)

    class Meta:
        model = PaidLeaveRequest
        fields = [
            'id',
            'employee',
            'employee_name',
            'employee_branch',
            'leave_date',
            'replace_with_date',
            'reason',
            'status',
            'approved_by',
            'approved_by_name',
            'created_at'
        ]

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'employee', 'login_time', 'logout_time', 'login_image', 'logout_image', 'status', 'date', 'total_hours', 'overtime_hours', 'break_hours']
        read_only_fields = ['id', 'employee', 'login_time', 'logout_time', 'status', 'total_hours', 'date', 'overtime_hours', 'break_hours']
        

class EmployeeMiniWithBranchSerializer(serializers.ModelSerializer):
    branch = BranchSerializer(read_only=True)
    role = RoleSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = ['id', 'name', 'branch', 'role']
        

class SalarySerializer(serializers.ModelSerializer):
    employee = EmployeeMiniWithBranchSerializer(read_only=True)
    gross_salary = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Salary
        fields = [
            'id',
            'employee',
            'month',
            'year',
            'base_salary',
            'overtime_salary',
            'commission',
            'deduction',
            'gross_salary',
            'paid_amount',
            'paid_at',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'employee', 'gross_salary', 'created_at', 'paid_amount', 'paid_at']
        
class MonthlyLeaveCreateSerializer(serializers.Serializer):
    leave_dates = serializers.ListField(
        child=serializers.DateField(),
        allow_empty=False,
        max_length=4,  # Max 4 leaves allowed
        error_messages={
            "max_length": "You can request max 4 leaves only."
        }
    )
    
class MonthlyLeaveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyLeaveItem
        fields = ['id', 'leave_date', 'status', 'approved_by']
        

class MonthlyLeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.CharField(source='employee.name', read_only=True)
    branch_id = serializers.IntegerField(source='employee.branch.id', read_only=True)
    branch_name = serializers.CharField(source='employee.branch.name', read_only=True)
    leaves = MonthlyLeaveItemSerializer(many=True, read_only=True)

    class Meta:
        model = MonthlyLeaveRequest
        fields = [
            'id',
            'employee_name',
            'aggregate_status',
            'branch_id',
            'branch_name',
            'created_at',
            'leaves'
        ]
