from django.contrib.auth import authenticate
from ..repositories.user_repository import UserRepository
from ..models import Company
from ..utils.custom_token import CustomRefreshToken


class AuthService:
    @staticmethod
    def register_user(**kwargs):
        role_name = kwargs.get("role")
        full_name = kwargs.get("full_name")
        email = kwargs.get("email")
        password = kwargs.get("password")

        if role_name == "Employee":
            company_uid = kwargs.get("company_uid")
            if not company_uid:
                raise ValueError("company_uid is required for Employee")
            company = UserRepository.get_company_by_uid(company_uid)
            role_obj = UserRepository.get_role_by_name("Employee")
            user = UserRepository.create_user(
                email=email,
                full_name=full_name,
                password=password,
                role=role_obj,
                company=company
            )

        elif role_name == "Administrator":
            company_name = kwargs.get("company_name")
            location = kwargs.get("location")
            if not company_name or not location:
                raise ValueError("company_name and location required for Administrator")
            role_obj = UserRepository.get_role_by_name("Administrator")
            company = Company.objects.create(company_name=company_name, location=location)
            user = UserRepository.create_user(
                email=email,
                full_name=full_name,
                password=password,
                role=role_obj,
                company=company
            )
        else:
            raise ValueError("Invalid role")

        # JWT tokens
        refresh = CustomRefreshToken.for_user(user)
        return {
            "user": user,
            "token": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }


class AuthLoginService:
    @staticmethod
    def login_user(email, password):
        user = authenticate(email=email, password=password)
        if not user:
            return None

        refresh = CustomRefreshToken.for_user(user)
        return {
            "user": user,
            "token": {
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }
        }
