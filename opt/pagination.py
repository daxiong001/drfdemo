from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class Home5PageNumberPagination(PageNumberPagination):
    page_size = 10  # 默认分页的每一页数据量
    max_page_size = 20  # 设置允许客户端通过地址栏参数调整的最大单页数据量
    page_query_param = "page"  # 地址栏上代表页码的变量名，默认是page
    page_size_query_param = "size"  # 地址栏上代表但也数据量的变量名，默认是page_size
