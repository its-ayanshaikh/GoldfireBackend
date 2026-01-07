"""
URL configuration for gf_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    
    # Role Management
    path('roles/', list_roles, name='list_roles'),
    path('roles/create/', create_role, name='create_role'),
    path('roles/update/<int:pk>/', update_role, name='update_role'),
    path('roles/delete/<int:pk>/', delete_role, name='delete_role'),
    
    # Employee Management
    path('', list_employees, name='list_employees'),
    path('create/', create_employee, name='create_employee'),
    path('update/<int:pk>/', update_employee, name='update_employee'),
    path('delete/<int:pk>/', delete_employee, name='delete_employee'),
    
    # Attendance Management
    path('attendance/login/', attendance_login, name='attendance-login'),
    path('attendance/logout/', attendance_logout, name='attendance-logout'),
    path('attendance/history/', my_attendance, name='attendance-history'),
    path('attendance/history/<int:emp_id>/', emp_attendance, name='attendance-history-by-id'),
    path('attendance/update/', update_attendance, name='attendance-update'),
    
    
    # Leave Management
    path('leaves/', list_leaves, name='list_leaves'),
    path('leaves/create/', create_leave, name='create_leave'),
    path('leaves/update/<int:pk>/', update_leave, name='update_leave'),
    path('leaves/delete/<int:pk>/', delete_leave, name='delete_leave'),
    
    # Leaves from Employee
    path('my-leaves/', employee_leaves_by_month, name='employee-leaves-by-month'),
    path('employee-leaves/', branch_employees_leaves, name='branch-employees-leaves'),
    
    # Leave Swap Requests
    path('leave-swap/create/', create_swap_request, name='create-swap'),
    path('leave-swap/<int:swap_id>/respond/', respond_swap_request, name='respond-swap'),
    path('swap/sent/', my_sent_swaps, name='my-sent-swaps'),
    path('swap/received/', my_received_swaps, name='my-received-swaps'),
    
    # Paid Leave Management
    path('paid-leave/request/list/', list_paid_leave_requests, name='list-paid-leave-requests'),
    path('paid-leave/request/', create_paid_leave_request, name='create-paid-leave-request'),
    path('paid-leave/status/', get_leave_status, name='get-leave-status'),
    path('paid-leave/request/<int:request_id>/update-status/', update_paid_leave_status, name='update-paid-leave-status'),
    
    #Monthly Leave Management
    path('monthly-leave/request/', create_monthly_leaves, name='create-monthly-leaves'),
    path('monthly-leave/requests/list/', monthly_leave_request_list, name='list-monthly-leave-requests'),
    path('monthly-leave/requests/list/admin/', monthly_leave_request_list_admin, name='list-monthly-leave-requests-admin'),
    path('monthly-leave/update/<int:leave_id>/', update_monthly_leave_item_status, name='update-monthly-leave-item-status'),
    
    
    # Salary Management
    path('salary/', get_salaries, name='get-salaries'),
    path('salary/update-payment/', update_salary_payment, name='update-salary-payment'),
]