from rest_framework.pagination import PageNumberPagination

class TaskPagination(PageNumberPagination):
    page_size = 12         # default items per page
    page_size_query_param = 'page_size'  # allow ?page_size=20
    max_page_size = 100
