from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from common.utils.response import success_response, error_response
from .serializers.login import LoginSerializer
from .serializers.register import RegisterSerializer
from .services.auth_service import AuthService, AuthLoginService


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = AuthService.register_user(**serializer.validated_data)
            user = result["user"]
            tokens = result["token"]

            data = {
                "user_id": str(user.uid),
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.role_name if user.role else None,
                "company": user.company.company_name if user.company else None,
                "token": tokens,
            }

            response = success_response(
                "User registered successfully.", data, status.HTTP_201_CREATED
            )

            # Set refresh token at  cookie
            response.set_cookie(
                key="refresh_token",
                value=tokens["refresh"],
                httponly=True,
                secure=False,  #  False for dev if not using HTTPS
                samesite="Strict",
                max_age=7 * 24 * 60 * 60,  # 1 week
            )

            login(request, user)
            return response

        except Exception as e:
            return error_response(str(e), status=400)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = AuthLoginService.login_user(**serializer.validated_data)
        if not result:
            return error_response("Invalid email or password", status=401)

        user = result["user"]
        tokens = result["token"]

        data = {
            "user_id": str(user.uid),
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role.role_name if user.role else None,
            "company": user.company.company_name if user.company else None,
            "token": tokens,
        }

        response = success_response("Login successful", data, status.HTTP_200_OK)

        # Set refresh token at cookie
        response.set_cookie(
            key="refresh_token",
            value=tokens["refresh"],
            httponly=True,
            secure=False,  #  False for dev if not using HTTPS
            samesite="Strict",
            max_age=7 * 24 * 60 * 60,  # 1 week
        )

        login(request, user)
        return response


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return error_response("Refresh token not provided", status=400)

            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = success_response("Logout successful")
            response.delete_cookie("refresh_token")
            return response

        except Exception as e:
            return error_response("Logout failed", str(e), status=400)
