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
    # RACK MANAGEMENT
    path('racks/', list_racks, name='list_racks'),
    path('racks/create/', create_rack, name='create_rack'),
    path('racks/<int:rack_id>/update/', update_rack, name='update_rack'),
    path('racks/<int:rack_id>/delete/', delete_rack, name='delete_rack'),
    
    # PRODUCT LIST WITH RACKS AND QUANTITIES
    path('allocate-rack/', allocate_rack, name='allocate_rack'),
    path('products/list/', product_list, name='product_list'),

    # BRANCH EMPLOYEES AND PRODUCT SEARCH
    path('employees/', get_branch_employees, name='get_branch_employees'),
    path('search-products/', search_products, name='search_products'),
    
    # TRANSFER PRODUCT BETWEEN BRANCHES
    path('transfers/create/', create_transfer_request, name='create_transfer_request'),
    path('transfer/update/<int:transfer_id>/', update_transfer_status, name='update_transfer_status'),
    path('transfers/sent/', sent_transfers, name='sent_transfers'),
    path('transfers/received/', received_transfers, name='received_transfers'),

    # BILL MANAGEMENT
    path('bills/', bill_list, name='bills'),
    path('bills/all/', bill_list_admin, name='bills_all'),
    path('bills/create/', create_bill, name='create_bill'),
    path('bills/search/', bill_search, name='bill_search'),
    path('bill/return/', create_return_bill, name='create_return_bill'),
    path('bills-show/', bills_show, name='bills_show'),
    path('replace/create/', create_replacement, name='create_replacement'),
    
    # CUSTOMER MANAGEMENT
    path('customers/', customer_list, name='customer_list'),
    path('due/update/', pay_bill_due, name='pay_bill_due'),
    path('customers/<int:pk>/bills/', customer_details_with_bills, name='customer_details_with_bills'),
    
]