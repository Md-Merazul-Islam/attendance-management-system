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
        # Create user
        user = User.objects.create_user(
            email="logout@example.com",
            full_name="Logout User",
            password="LogoutPass123",
            role=self.employee_role,
            company=self.company
        )
        
        # Login to get token
        login_payload = {"email": "logout@example.com", "password": "LogoutPass123"}
        login_response = self.client.post(self.login_url, login_payload, format='json')
        
        # Debug: Print the login response
        print("\n=== LOGIN RESPONSE ===")
        print(f"Status: {login_response.status_code}")
        print(f"Data: {login_response.data}")
        print(f"Cookies: {login_response.cookies}")
        
        # Check if login was successful
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        
        # Extract token from login response
        token = login_response.data["data"]["token"]
        print(f"\n=== TOKEN ===")
        print(f"Token: {token}")
        
        # Method 1: Try with Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # Method 2: Also set refresh token cookie if it exists
        if "refresh_token" in login_response.cookies:
            self.client.cookies["refresh_token"] = login_response.cookies["refresh_token"].value

        # Now logout with authentication
        print("\n=== LOGOUT REQUEST ===")
        response = self.client.post(self.logout_url, format='json')
        
        print(f"\n=== LOGOUT RESPONSE ===")
        print(f"Status: {response.status_code}")
        print(f"Data: {response.data}")
        
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")