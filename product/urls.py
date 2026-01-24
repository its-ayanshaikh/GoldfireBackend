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
    # CATEGORY URLs
    path('categories/', get_categories, name='get-categories'),
    
    # COMMISSION URLs
    path('commission/<int:category_id>/', get_category_commission, name='get-category-commission'),
    path('commission/list/', commission_list, name='commission-list'),
    path('commission/categories/', commission_categories, name='commission-list'),
    path('commission/create/', commission_create, name='commission-create'),
    path('commission/update/<int:pk>/', commission_update, name='commission-update'),
    path('commission/delete/<int:pk>/', commission_delete, name='commission-delete'),

    # HSN URLs
    path('hsn/create/', create_hsn, name='create_hsn'),
    path('hsn/list/', list_hsn, name='list_hsn'),  # ?category_id=1
    path('hsn/update/<int:hsn_id>/', update_hsn, name='update_hsn'),
    path('hsn/delete/<int:hsn_id>/', delete_hsn, name='delete_hsn'),
    path('<int:category_id>/hsn&comission/', category_hsn_commission, name='category-hsn-commission'),
    
    # SUBCATEGORY URLs
    path('categories/<int:category_id>/subcategories/', subcategories_by_category, name='subcategory-by-category'),
    path('subcategories/create/', create_subcategory, name='subcategory-create'),
    path('subcategories/<int:pk>/update/', update_subcategory, name='subcategory-update'),
    path('subcategories/<int:pk>/delete/', delete_subcategory, name='subcategory-delete'),
    
    # TYPE URLs
    path('type/create/', create_type, name='create_type'),
    path('type/list/<int:category_id>/', list_types, name='list_types'),
    path('type/update/<int:type_id>/', update_type, name='update_type'),
    path('type/delete/<int:type_id>/', delete_type, name='delete_type'),
    
    # BRAND URLs
    path('brand/create/', create_brand, name='create-brand'),
    path('brand/list/', list_brands, name='list-brands'),
    path('brand/category/<int:category_id>/', brands_by_category, name='brands-by-category'),
    # path('brand/subcategory/<int:subcategory_id>/', brands_by_subcategory, name='brands-by-subcategory'),
    path('brand/update/<int:brand_id>/', update_brand, name='update-brand'),
    path('brand/delete/<int:brand_id>/', delete_brand, name='delete-brand'),
    
    # SUBBRAND URLs
    path('subbrands/create/', create_subbrand, name='create_subbrand'),
    path('subbrands/<int:subcategory_id>/', list_subbrands, name='list_subbrands'),
    path('subbrands/update/<int:subbrand_id>/', update_subbrand, name='update_subbrand'),
    path('subbrands/delete/<int:subbrand_id>/', delete_subbrand, name='delete_subbrand'),
    
    # MODEL URLs
    path('models/<int:subbrand_id>/', list_models, name='list_models'),
    path('models/create/', create_model, name='create_model'),
    path('models/<int:pk>/update/', update_model, name='update_model'),
    path('models/<int:pk>/delete/', delete_model, name='delete_model'),
    
    # PRODUCT URLs
    path('create/', create_product, name='create_product'),
    path('list/', list_products, name='list_products'),  # ?category_id=1
    path('<int:product_id>/', product_details, name='product_details'),  # ?category_id=1
    path('update/<int:product_id>/', update_product, name='update_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path("dropdown/", product_dropdown_list, name="product-dropdown"),
    path("<int:product_id>/variants/", product_variants_dropdown, name="product-variants-dropdown"),
]