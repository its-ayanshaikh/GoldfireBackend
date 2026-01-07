from rest_framework.pagination import PageNumberPagination

class EmployeePagination(PageNumberPagination):
    page_size = 20                # 20 records per page
    page_size_query_param = 'page_size'  # optional
    max_page_size = 100
