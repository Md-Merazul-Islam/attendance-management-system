from ..models import User, Role, Company

class UserRepository:
    @staticmethod
    def get_role_by_name(role_name: str):
        return Role.objects.get(role_name=role_name)

    @staticmethod
    def get_company_by_uid(company_uid):
        return Company.objects.get(uid=company_uid)

    @staticmethod
    def create_user(email, full_name, password, role=None, company=None):
        user = User.objects.create_user(
            email=email,
            full_name=full_name,
            password=password,
            role=role,
            company=company
        )
        return user

    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()
