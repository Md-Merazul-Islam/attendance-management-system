from django.test import TestCase
from django.db import IntegrityError
from django.utils import timezone
from apps.attendance.models import Attendance
from apps.auths.models import User, Role
from apps.companies.models import Company
from datetime import date, timedelta
import uuid


class AttendanceModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # Create role
        self.role = Role.objects.create(role_name="Employee")
        
        # Create company
        self.company = Company.objects.create(
            company_name="Test Company",
            location="Dhaka"
        )
        
        # Create user
        self.user = User.objects.create_user(
            email="test@example.com",
            full_name="Test User",
            password="testpass123",
            role=self.role,
            company=self.company
        )
        
        # Create attendance
        self.attendance = Attendance.objects.create(
            user=self.user,
            code="QR",
            is_qr=True,
            date=date.today()
        )
    
    def test_attendance_creation(self):
        """Test that attendance can be created successfully"""
        self.assertIsNotNone(self.attendance)
        self.assertEqual(self.attendance.user, self.user)
        self.assertEqual(self.attendance.code, "QR")
        self.assertTrue(self.attendance.is_qr)
        self.assertFalse(self.attendance.is_nfc)
    
    def test_attendance_uid_generation(self):
        """Test that UID is automatically generated"""
        self.assertIsNotNone(self.attendance.uid)
        self.assertIsInstance(self.attendance.uid, uuid.UUID)
    
    def test_attendance_uid_uniqueness(self):
        """Test that each attendance has a unique UID"""
        attendance2 = Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=1)
        )
        self.assertNotEqual(self.attendance.uid, attendance2.uid)
    
    def test_attendance_created_at_auto_set(self):
        """Test that created_at is automatically set"""
        self.assertIsNotNone(self.attendance.created_at)
        self.assertLessEqual(self.attendance.created_at, timezone.now())
    
    def test_attendance_str_representation(self):
        """Test the string representation of attendance"""
        expected = f"{self.user.email} - {self.attendance.date}"
        self.assertIn(str(self.attendance.date), str(self.attendance))
    
    def test_attendance_with_qr_code(self):
        """Test attendance with QR code"""
        qr_attendance = Attendance.objects.create(
            user=self.user,
            code="QR",
            is_qr=True,
            date=date.today() - timedelta(days=2)
        )
        self.assertEqual(qr_attendance.code, "QR")
        self.assertTrue(qr_attendance.is_qr)
        self.assertFalse(qr_attendance.is_nfc)
    
    def test_attendance_with_nfc_code(self):
        """Test attendance with NFC code"""
        nfc_attendance = Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=3)
        )
        self.assertEqual(nfc_attendance.code, "NFC")
        self.assertTrue(nfc_attendance.is_nfc)
        self.assertFalse(nfc_attendance.is_qr)
    
    def test_attendance_code_choices(self):
        """Test that only valid code choices are accepted"""
        field = Attendance._meta.get_field('code')
        choices = [choice[0] for choice in field.choices]
        self.assertIn("QR", choices)
        self.assertIn("NFC", choices)
        self.assertEqual(len(choices), 2)
    
    def test_attendance_unique_together_constraint(self):
        """Test that user cannot have multiple attendances on same date"""
        with self.assertRaises(IntegrityError):
            Attendance.objects.create(
                user=self.user,
                code="NFC",
                is_nfc=True,
                date=date.today() 
            )
    
    def test_attendance_different_users_same_date(self):
        """Test that different users can have attendance on same date"""
        user2 = User.objects.create_user(
            email="user2@example.com",
            full_name="User Two",
            password="testpass123",
            role=self.role,
            company=self.company
        )
        
        attendance2 = Attendance.objects.create(
            user=user2,
            code="NFC",
            is_nfc=True,
            date=date.today()  
        )
        
        self.assertIsNotNone(attendance2)
        self.assertEqual(attendance2.user, user2)
    
    def test_attendance_ordering(self):
        """Test that attendances are ordered by date descending"""
        # Create attendances with different dates
        att1 = Attendance.objects.create(
            user=self.user,
            code="QR",
            is_qr=True,
            date=date.today() - timedelta(days=5)
        )
        att2 = Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=1)
        )
        
        attendances = list(Attendance.objects.all())
        # Most recent should be first
        self.assertEqual(attendances[0].date, date.today())
        self.assertEqual(attendances[-1].date, date.today() - timedelta(days=5))
    
    def test_attendance_user_deletion_cascade(self):
        """Test that deleting user also deletes their attendances"""
        attendance_uid = self.attendance.uid
        user_uid = self.user.uid
        
        # Delete the user
        self.user.delete()
        
        # Check that user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(uid=user_uid)
        
        # Check that attendance is also deleted (CASCADE)
        with self.assertRaises(Attendance.DoesNotExist):
            Attendance.objects.get(uid=attendance_uid)
    
    def test_attendance_update(self):
        """Test updating attendance details"""
        self.attendance.code = "NFC"
        self.attendance.is_nfc = True
        self.attendance.is_qr = False
        self.attendance.save()
        
        updated_attendance = Attendance.objects.get(uid=self.attendance.uid)
        self.assertEqual(updated_attendance.code, "NFC")
        self.assertTrue(updated_attendance.is_nfc)
        self.assertFalse(updated_attendance.is_qr)
    
    def test_attendance_filter_by_user(self):
        """Test filtering attendances by user"""
        # Create another user
        user2 = User.objects.create_user(
            email="user2@example.com",
            full_name="User Two",
            password="testpass123",
            role=self.role,
            company=self.company
        )
        
        # Create attendances for both users
        Attendance.objects.create(
            user=self.user,
            code="QR",
            is_qr=True,
            date=date.today() - timedelta(days=1)
        )
        Attendance.objects.create(
            user=user2,
            code="NFC",
            is_nfc=True,
            date=date.today()
        )
        
        user1_attendances = Attendance.objects.filter(user=self.user)
        self.assertEqual(user1_attendances.count(), 2)  # 1 from setUp + 1 new
    
    def test_attendance_filter_by_code(self):
        """Test filtering attendances by code type"""
        Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=1)
        )
        Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=2)
        )
        
        qr_attendances = Attendance.objects.filter(code="QR")
        nfc_attendances = Attendance.objects.filter(code="NFC")
        
        self.assertEqual(qr_attendances.count(), 1)
        self.assertEqual(nfc_attendances.count(), 2)
    
    def test_attendance_filter_by_date_range(self):
        """Test filtering attendances by date range"""
        # Create attendances over multiple days
        for i in range(1, 6):
            Attendance.objects.create(
                user=self.user,
                code="QR",
                is_qr=True,
                date=date.today() - timedelta(days=i)
            )
        
        start_date = date.today() - timedelta(days=3)
        end_date = date.today()
        
        attendances = Attendance.objects.filter(
            date__range=[start_date, end_date]
        )
        self.assertEqual(attendances.count(), 4)  # 1 from setUp + 3 in range
    
    def test_attendance_related_name(self):
        """Test accessing attendances through user's related name"""
        Attendance.objects.create(
            user=self.user,
            code="NFC",
            is_nfc=True,
            date=date.today() - timedelta(days=1)
        )
        
        user_attendances = self.user.attendances.all()
        self.assertEqual(user_attendances.count(), 2)
    
    def test_attendance_boolean_defaults(self):
        """Test that boolean fields have correct defaults"""
        attendance = Attendance.objects.create(
            user=self.user,
            code="QR",
            date=date.today() - timedelta(days=10)
        )
        
        self.assertFalse(attendance.is_nfc)
        self.assertFalse(attendance.is_qr)
    
    def test_attendance_date_field(self):
        """Test that date field works correctly"""
        test_date = date(2024, 1, 15)
        attendance = Attendance.objects.create(
            user=self.user,
            code="QR",
            is_qr=True,
            date=test_date
        )
        
        self.assertEqual(attendance.date, test_date)
        self.assertIsInstance(attendance.date, date)
        
        
        
