from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import BranchSerializer
from .models import Branch, Company
from rest_framework import status
from accounts.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from decimal import Decimal
from pos.models import Bill, BillItem, Customer
from employee.models import Employee, SalesCommission

User = get_user_model()

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_branches(request):
    """
    Get all branches for company id=1
    Include if POS user exists and its ID
    """
    try:
        company = Company.objects.get(id=1)
    except Company.DoesNotExist:
        return Response(
            {"error": "Company with id=1 not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    branches = Branch.objects.filter(company=company)
    serializer = BranchSerializer(branches, many=True)

    data = []
    for branch in serializer.data:
        branch_id = branch['id']
        pos_user = User.objects.filter(branch_id=branch_id, role='cashier').first()

        branch_info = {
            **branch,
            "pos_user_exists": bool(pos_user),
            "pos_user_id": pos_user.id if pos_user else None
        }
        data.append(branch_info)

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_branch(request):
    """
    Create new branch for company id=1
    """
    try:
        company = Company.objects.get(id=1)
    except Company.DoesNotExist:
        return Response({"error": "Company with id=1 not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()
    data['company'] = company.id  # force assign company id=1
    serializer = BranchSerializer(data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_branch(request, pk):
    """
    Update a branch by ID
    """
    try:
        branch = Branch.objects.get(id=pk, company_id=1)
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)

    company = Company.objects.get(id=1)
    data = request.data.copy()
    
    data['company'] = company.id # force assign company id=1
    
    serializer = BranchSerializer(branch, data=data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_branch(request, pk):
    """
    Delete a branch by ID (company_id=1)
    Also deletes associated POS user (if exists)
    """
    try:
        branch = Branch.objects.get(id=pk, company_id=1)
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found"}, status=status.HTTP_404_NOT_FOUND)

    # delete POS user if exists
    pos_user = User.objects.filter(branch=branch, role='cashier').first()
    if pos_user:
        pos_user.delete()

    # now delete branch
    branch.delete()

    return Response(
        {"message": "Branch and associated POS user (if any) deleted successfully"},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_pos_user(request):
    """
    Create a POS user (cashier) for a branch.
    Only one POS user per branch is allowed.
    """
    branch_id = request.data.get('branch_id')
    username = request.data.get('username')
    password = request.data.get('password')

    # validation
    if not branch_id or not username or not password:
        return Response(
            {"error": "branch_id, username, and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # check if branch exists
    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

    # check if already a POS user exists for this branch
    if User.objects.filter(branch=branch, role='cashier').exists():
        return Response(
            {"error": "This branch already has a POS user."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # create new POS user with hashed password
    user = User.objects.create(
        username=username,
        password=make_password(password),  # hash password
        role='cashier',
        branch=branch
    )

    return Response({
        "message": "POS user created successfully.",
        "user_id": user.id,
        "username": user.username,
        "branch_id": branch.id
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_pos_user_password(request):
    """
    Update the password for a POS user using branch_id
    """
    branch_id = request.data.get('branch_id')
    password = request.data.get('password')

    if not branch_id or not password:
        return Response(
            {"error": "branch_id and password are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        branch = Branch.objects.get(id=branch_id)
    except Branch.DoesNotExist:
        return Response({"error": "Branch not found."}, status=status.HTTP_404_NOT_FOUND)

    # get POS user for this branch
    try:
        user = User.objects.get(branch=branch, role='cashier')
    except User.DoesNotExist:
        return Response({"error": "POS user not found for this branch."}, status=status.HTTP_404_NOT_FOUND)

    # update password (hashed)
    user.password = make_password(password)
    user.save()

    return Response({
        "message": "Password updated successfully for POS user.",
        "user_id": user.id,
        "branch_id": branch.id
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """
    Dashboard API with stats, charts, customer analytics, and employee of the month
    Query Params: branch_id (optional) - filter by branch
    """
    branch_id = request.query_params.get('branch_id')
    
    # Base querysets with optional branch filter
    bill_qs = Bill.objects.all()
    employee_qs = Employee.objects.filter(status='active')
    
    if branch_id:
        bill_qs = bill_qs.filter(branch_id=branch_id)
        employee_qs = employee_qs.filter(branch_id=branch_id)
    
    # Exclude default customer (phone = 0000000000)
    customer_qs = Customer.objects.exclude(phone='0000000000')
    
    # ========================================
    # 1. SUMMARY STATS
    # ========================================
    total_sales = bill_qs.count()
    total_revenue = bill_qs.aggregate(total=Sum('final_amount'))['total'] or Decimal('0')
    total_customers = customer_qs.count()
    total_employees = employee_qs.count()
    
    summary_stats = {
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "total_customers": total_customers,
        "total_employees": total_employees
    }
    
    # ========================================
    # 2. SALES ANALYTICS - Last 6 Months Revenue Trends
    # ========================================
    now = timezone.now()
    six_months_ago = now - relativedelta(months=6)
    
    revenue_trends = (
        bill_qs
        .filter(date__gte=six_months_ago)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(revenue=Sum('final_amount'), sales_count=Count('id'))
        .order_by('month')
    )
    
    sales_analytics = [
        {
            "month": entry['month'].strftime('%Y-%m') if entry['month'] else None,
            "month_name": entry['month'].strftime('%B %Y') if entry['month'] else None,
            "revenue": float(entry['revenue'] or 0),
            "sales_count": entry['sales_count']
        }
        for entry in revenue_trends
    ]
    
    # ========================================
    # 3. TOP SELLING PRODUCTS - This Month (Top 5)
    # ========================================
    current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    bill_item_qs = BillItem.objects.filter(is_returned=False)
    if branch_id:
        bill_item_qs = bill_item_qs.filter(bill__branch_id=branch_id)
    
    top_products = (
        bill_item_qs
        .filter(bill__date__gte=current_month_start)
        .values('product__id', 'product__name')
        .annotate(
            total_qty=Sum('qty'),
            total_revenue=Sum('final_amount')
        )
        .order_by('-total_qty')[:5]
    )
    
    top_selling_products = [
        {
            "product_id": p['product__id'],
            "product_name": p['product__name'],
            "total_qty_sold": p['total_qty'],
            "total_revenue": float(p['total_revenue'] or 0)
        }
        for p in top_products
    ]
    
    # ========================================
    # 4. CUSTOMER ANALYTICS
    # ========================================
    # Get customer purchase stats (only for bills in selected branch if filtered)
    customer_stats = (
        customer_qs
        .exclude(phone='0000000000')
        .annotate(
            total_purchases=Count('bills', filter=Q(bills__branch_id=branch_id) if branch_id else Q()),
            total_spent=Sum('bills__final_amount', filter=Q(bills__branch_id=branch_id) if branch_id else Q()),
            last_purchase=F('bills__date')
        )
    )
    
    # Calculate last purchase properly
    from django.db.models import Max
    customer_data = (
        customer_qs
        .exclude(phone='0000000000')
        .annotate(
            total_purchases=Count('bills', filter=Q(bills__branch_id=branch_id) if branch_id else Q()),
            total_spent=Sum('bills__final_amount', filter=Q(bills__branch_id=branch_id) if branch_id else Q()),
            last_purchase=Max('bills__date', filter=Q(bills__branch_id=branch_id) if branch_id else Q())
        )
    )
    
    # Segment customers
    # Frequent: 10+ purchases, Regular: 3-9 purchases, Lost: no purchase in last 90 days
    ninety_days_ago = now - relativedelta(days=90)
    
    frequent_customers = []
    regular_customers = []
    lost_customers = []
    
    for c in customer_data:
        purchases = c.total_purchases or 0
        last_date = c.last_purchase
        
        customer_info = {
            "id": c.id,
            "name": c.name,
            "phone": c.phone,
            "total_purchases": purchases,
            "total_spent": float(c.total_spent or 0),
            "last_purchase": last_date.strftime('%Y-%m-%d') if last_date else None,
        }
        
        if purchases >= 10:
            customer_info["status"] = "frequent"
            frequent_customers.append(customer_info)
        elif purchases >= 3:
            customer_info["status"] = "regular"
            regular_customers.append(customer_info)
        elif last_date and last_date < ninety_days_ago:
            customer_info["status"] = "lost"
            lost_customers.append(customer_info)
        elif purchases > 0 and last_date and last_date >= ninety_days_ago:
            customer_info["status"] = "regular"
            regular_customers.append(customer_info)
        elif purchases > 0:
            customer_info["status"] = "lost"
            lost_customers.append(customer_info)
    
    customer_analytics = {
        "frequent_count": len(frequent_customers),
        "regular_count": len(regular_customers),
        "lost_count": len(lost_customers),
        "total_customers": len(frequent_customers) + len(regular_customers) + len(lost_customers),
        "segments": {
            "frequent": frequent_customers[:2],  # Top 2 from each segment
            "regular": regular_customers[:2],
            "lost": lost_customers[:2]
        }
    }
    
    # ========================================
    # 5. EMPLOYEE OF THE MONTH + TOP 3 MORE
    # ========================================
    current_month = now.strftime('%Y-%m')
    
    # Get commission data for current month
    commission_qs = SalesCommission.objects.filter(month=current_month)
    if branch_id:
        commission_qs = commission_qs.filter(salesperson__branch_id=branch_id)
    
    top_employees_data = commission_qs.order_by('-total_commission')[:4]
    
    top_employees = []
    for idx, sc in enumerate(top_employees_data):
        emp = sc.salesperson
        emp_data = {
            "employee_id": emp.id,
            "name": emp.name,
            "role": emp.role.name if emp.role else None,
            "branch": emp.branch.name if emp.branch else None,
            "branch_id": emp.branch.id if emp.branch else None,
            "total_sales": float(sc.total_sales or 0),
            "total_commission": float(sc.total_commission or 0),
            "is_employee_of_month": idx == 0
        }
        top_employees.append(emp_data)
    
    employee_of_month = top_employees[0] if top_employees else None
    other_top_employees = top_employees[1:4] if len(top_employees) > 1 else []
    
    employee_analytics = {
        "employee_of_month": employee_of_month,
        "other_top_employees": other_top_employees
    }
    
    # ========================================
    # FINAL RESPONSE
    # ========================================
    return Response({
        "summary_stats": summary_stats,
        "sales_analytics": sales_analytics,
        "top_selling_products": top_selling_products,
        "customer_analytics": customer_analytics,
        "employee_analytics": employee_analytics,
        "filters_applied": {
            "branch_id": int(branch_id) if branch_id else None
        }
    }, status=status.HTTP_200_OK)
