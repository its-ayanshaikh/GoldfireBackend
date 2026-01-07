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
from django.conf import settings
from .views import *

urlpatterns = [
    
    # TASK MANAGEMENT
    path('', list_tasks, name='list_tasks'),
    path('create/', create_task, name='create_task'),
    path('<int:pk>/', get_task, name='get_task'),
    path('<int:pk>/update/', update_task, name='update_task'),
    path('<int:pk>/delete/', delete_task, name='delete_task'),
    path('list/submissions/', list_all_submissions, name='list_all_submissions'),
    
    
    # TASK SUBMISSION
    path('employee-task/', employee_today_tasks, name='employee_today_tasks'),
    path('submit/', submit_task, name='submit_task'),
    path('submitted-tasks/', today_submitted_tasks, name='today_submitted_tasks'),
]
