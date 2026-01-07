from rest_framework.pagination import PageNumberPagination

class BillPagination(PageNumberPagination):
    page_size = 20  # default items per page
    page_size_query_param = 'page_size'  # frontend can control size like ?page_size=20
    max_page_size = 100  # prevent heavy load


class CustomerPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100