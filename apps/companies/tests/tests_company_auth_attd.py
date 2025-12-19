from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.auths.models import Role, User
from apps.companies.models import Company
from apps.attendance.models import Attendance
from datetime import date

class AuthAndCompanyTestCase(APITestCase):

    def setUp(self):
        """Setup Roles, Company and URLs"""
        # Roles
        self.employee_role = Role.objects.create(role_name="Employee")
        self.admin_role = Role.objects.create(role_name="Administrator")

        # Company
        self.company = Company.objects.create(company_name="TestCorp", location="USA")

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.company_list_url = reverse("company-list")  # adjust your URL names
        self.company_detail_url = lambda uid: reverse("company-detail", args=[uid])
        self.update_company_url = lambda uid: reverse("company-update", args=[uid])

    # -------------------------
    # User Registration
    # -------------------------
    def test_employee_registration_success(self):
        payload = {
            "role": "Employee",
            "full_name": "John Doe",
            "email": "john@example.com",
            "password": "TestPass123",
            "company_uid": str(self.company.uid)
        }
        response = self.client.post(self.register_url, payload, format="json")
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
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data["data"])
        self.assertEqual(response.data["data"]["role"], "Administrator")
        self.assertEqual(response.data["data"]["company"], "AdminCorp")

    # -------------------------
    # Login / Logout
    # -------------------------
    def test_login_success(self):
        user = User.objects.create_user(
            email="login@example.com",
            full_name="Login User",
            password="LoginPass123",
            role=self.employee_role,
            company=self.company
        )
        payload = {"email": "login@example.com", "password": "LoginPass123"}
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data["data"])
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
        response = self.client.post(self.login_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_success(self):
        user = User.objects.create_user(
            email="logout@example.com",
            full_name="Logout User",
            password="LogoutPass123",
            role=self.employee_role,
            company=self.company
        )
        # login first
        login_payload = {"email": "logout@example.com", "password": "LogoutPass123"}
        response = self.client.post(self.login_url, login_payload, format="json")
        self.client.cookies["refresh_token"] = response.cookies["refresh_token"].value

        response = self.client.post(self.logout_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout successful")

    # -------------------------
    # Company APIs
    # -------------------------
    def test_company_list_for_admin(self):
        admin_user = User.objects.create_user(
            email="admin2@example.com",
            full_name="Admin Two",
            password="AdminPass123",
            role=self.admin_role,
            company=self.company
        )
        self.client.force_authenticate(admin_user)
        response = self.client.get(self.company_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_company_detail_for_admin(self):
        admin_user = User.objects.create_user(
            email="admin3@example.com",
            full_name="Admin Three",
            password="AdminPass123",
            role=self.admin_role,
            company=self.company
        )
        self.client.force_authenticate(admin_user)
        response = self.client.get(self.company_detail_url(self.company.uid))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["uid"], str(self.company.uid))

    def test_update_company_info(self):
        admin_user = User.objects.create_user(
            email="admin4@example.com",
            full_name="Admin Four",
            password="AdminPass123",
            role=self.admin_role,
            company=self.company
        )
        self.client.force_authenticate(admin_user)
        payload = {"company_name": "NewNameCorp", "location": "Canada"}
        response = self.client.put(self.update_company_url(self.company.uid), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["company"]["company_name"], "NewNameCorp")
        self.assertEqual(response.data["company"]["location"], "Canada")

    # -------------------------
    # Attendance (Optional)
    # -------------------------
    def test_create_attendance_for_employee(self):
        employee = User.objects.create_user(
            email="attend@example.com",
            full_name="Attendance User",
            password="Pass123",
            role=self.employee_role,
            company=self.company
        )
        self.client.force_authenticate(employee)
        payload = {"is_nfc": True, "is_qr": False, "code": "NFC", "date": str(date.today())}
        response = self.client.post(reverse("attendance-create"), payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_400_BAD_REQUEST])
