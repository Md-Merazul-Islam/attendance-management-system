from rest_framework.views import APIView
from common.utils.response import success_response, error_response

class BaseAPIView(APIView):
    def success(self, data=None, message="Success", status=200):
        return success_response(data=data, message=message, status=status)

    def error(self, message="Error", error=None, status=400):
        return error_response(message=message, error=error, status=status)
