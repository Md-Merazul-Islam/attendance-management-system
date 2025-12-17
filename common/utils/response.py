from rest_framework.response import Response

def success_response( message="Success",data=None, status=200):
    return Response({
        "success": True,
        "statusCode": status,
        "message": message,
        "data": data or {}
    }, status=status)


def error_response(message="Error", error=None, status=400):
    return Response({
        "success": False,
        "statusCode": status,
        "message": message,
        "error": error or {}
    }, status=status)
