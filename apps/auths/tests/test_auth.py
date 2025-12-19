from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.auths.models import Role, User
from apps.companies.models import Company

class AuthTestCase(APITestCase):

    def setUp(self):
        # Create Roles
        self.employee_role = Role.objects.create(role_name="Employee")
        self.admin_role = Role.objects.create(role_name="Administrator")
        
        # Create a company for Employee registration
        self.company = Company.objects.create(company_name="TestCorp", location="USA")

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_employee_registration_success(self):
        payload = {
            "role": "Employee",
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "TestPass123",
            "company_uid": str(self.company.uid)
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["role"], "Employee")

    def test_admin_registration_success(self):
        payload = {
            "role": "Administrator",
            "full_name": "Admin User",
            "email": "admin@example.com",
            "password": "AdminPass123",
            "company_name": "AdminCorp",
            "location": "UK"
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["role"], "Administrator")
        self.assertEqual(response.data["data"]["company"], "AdminCorp")

    def test_login_success(self):
        # First register a user
        user = User.objects.create_user(
            email="login@example.com",
            full_name="Login User",
            password="LoginPass123",
            role=self.employee_role,
            company=self.company
        )
        payload = {"email": "login@example.com", "password": "LoginPass123"}
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data["data"])
        # Check cookie
        self.assertIn("refresh_token", response.cookies)

    def test_login_failure_invalid_password(self):
        user = User.objects.create_user(
            email="fail@example.com",
            full_name="Fail User",
            password="RightPass123",
            role=self.employee_role,
            company=self.company
        )
        payload = {"email": "fail@example.com", "password": "WrongPass"}
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        user = User.objects.create_user(
            email="logout@example.com",
            full_name="Logout User",
            password="LogoutPass123",
            role=self.employee_role,
            company=self.company
        )
        # login to set cookie
        login_payload = {"email": "logout@example.com", "password": "LogoutPass123"}
        response = self.client.post(self.login_url, login_payload, format='json')
        self.client.cookies["refresh_token"] = response.cookies["refresh_token"].value

        # Logout
        response = self.client.post(self.logout_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")
