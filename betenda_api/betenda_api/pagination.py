from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class LargeResultsSetPagination(PageNumberPagination):
    '''
    Get 100 posts at once and a max page size of 1000
    '''
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'pages_count': math.ceil(self.page.paginator.count/int(self.request.GET.get('page_size', self.page_size))),
            'page': int(self.request.GET.get('page', DEFAULT_STANDARD_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })

DEFAULT_STANDARD_PAGE = 1
DEFAULT_STANDARD_PAGE_SIZE = 20


class StandardResultsSetPagination(PageNumberPagination):
    '''
    Get 20 posts at once and a max page size of 200
    '''
    page = DEFAULT_STANDARD_PAGE
    page_size = DEFAULT_STANDARD_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = 200

    def get_paginated_response(self, data):
        return Response({
            'total': self.page.paginator.count,
            'pages_count': math.ceil(self.page.paginator.count/int(self.request.GET.get('page_size', self.page_size))),
            'page': int(self.request.GET.get('page', DEFAULT_STANDARD_PAGE)),
            'page_size': int(self.request.GET.get('page_size', self.page_size)),
            'results': data
        })