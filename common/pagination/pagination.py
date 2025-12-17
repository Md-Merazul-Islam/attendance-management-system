from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            "success": True,
            "message": "All data retrieved successfully",
            "meta": {
                "page": self.page.number,
                "limit": self.page.paginator.per_page,
                "total": self.page.paginator.count,
                "totalPage": self.page.paginator.num_pages,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
            },
            "data": data,
        })
