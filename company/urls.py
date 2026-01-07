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
    
    # Branch Management
    path('', list_branches, name='list_branches'),         # GET
    path('create/', create_branch, name='create_branch'),  # POST
    path('update/<int:pk>/', update_branch, name='update_branch'),  # PUT/PATCH
    path('delete/<int:pk>/', delete_branch, name='delete_branch'),  # DELETE

    #POS User Management
    path('pos-user/create/', create_pos_user, name='create_pos_user'),
    path('pos-user/update-password/', update_pos_user_password, name='update_pos_user_password'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),  # GET with ?branch_id=1
]
