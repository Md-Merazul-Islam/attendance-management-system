from rest_framework import generics,filters,permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class BaseListAPIView(generics.ListAPIView):
    pagination_class = None
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        # Get filtered queryset
        queryset = self.filter_queryset(self.get_queryset())

        # Generate message
        model_name = queryset.model.__name__
        success_message = f"All {model_name.lower()}s fetched successfully"

        # Store message in request
        request.list_message = success_message

        # Check if pagination is enabled
        if self.pagination_class is not None:
            # Paginate the queryset
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

        # No pagination - return all data
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            {
                "success": True,
                "statusCode": 200,
                "message": success_message,
                "data": serializer.data,
            }
        )


class BaseRetrieveAPIView(generics.RetrieveAPIView):
    """
    Base class for retrieve-only endpoints.
    Automatically generates success message based on model name.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        model_name = instance.__class__.__name__
        success_message = f"{model_name} fetched successfully"

        return Response(
            {
                "success": True,
                "statusCode": 200,
                "message": success_message,
                "data": serializer.data,
            }
        )


# class PackageRetrieveView(BaseRetrieveAPIView):
#     queryset = Package.objects.all()
#     serializer_class = PackageSerializer
